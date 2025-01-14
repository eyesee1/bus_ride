from typing import Any

from attr import define, field

from bus_ride import (
    Command,
    Event,
    Handler,
    HandlerReturnType,
    Receiver,
    ReceiverReturnType,
    ReturnMessage,
)


class IntentionallyFailingTestError(Exception):
    pass


@define
class FakeCommand(Command):
    what: str = field()
    how_many: int = field(default=1)


@define
class FakeCommand2(Command):
    what: str = field()
    how_many: int = field(default=1)


@define
class FakeFailingCommand(Command):
    what: str = field()
    how_many: int = field(default=1)


@define(frozen=True)
class FakeEvent(Event):
    data: Any = field()


@define
class FakeCommandWithNoReceiver(Command):
    data: Any = field()


@define(frozen=True)
class FakeEvent2(Event):
    data: Any = field()


class FakeFailingReceiver(Receiver):
    handles_command_cls = FakeFailingCommand

    def execute_command(self) -> ReceiverReturnType:
        raise IntentionallyFailingTestError


class FakeReceiver(Receiver):
    handles_command_cls = FakeCommand

    def execute_command(self) -> ReceiverReturnType:
        return [FakeEvent(data="We did the thing!")]


class FakeReceiver2(Receiver):
    handles_command_cls = FakeCommand2

    def execute_command(self) -> ReceiverReturnType:
        return [FakeEvent2(data="We did the thing!")]


class FakeHandler(Handler):
    handles_events = [FakeEvent]

    def handle_event(self) -> HandlerReturnType:
        return [
            ReturnMessage(data="Senpai would be so proud."),
        ]


class FakeHandler2(Handler):
    handles_events = [FakeEvent2]

    def handle_event(self) -> HandlerReturnType:
        return [
            ReturnMessage(data="Senpai would be so proud."),
        ]


@define(frozen=True)
class FakeFailingEvent(Event):
    data: Any = field()


@define(frozen=True)
class FakeEventWithNoHandler(Event):
    data: Any = field()


class FakeFailingHandler(Handler):
    handles_events = [FakeFailingEvent]

    def handle_event(self) -> HandlerReturnType:
        raise IntentionallyFailingTestError
