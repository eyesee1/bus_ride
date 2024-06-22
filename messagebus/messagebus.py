import logging
from collections import defaultdict
from collections.abc import Callable, Sequence
from typing import Any, Literal, TypeVar, Union, final

from attrs import define, field
from attrs.validators import in_

from .command import Command
from .event import Event
from .exceptions import MessageBusConfigurationError, UnknownMessageTypeError
from .handler import Handler, HandlerReturnType, HandlerType
from .receiver import Receiver, ReceiverReturnType
from .returnmessage import ReturnMessage

logger = logging.getLogger(__name__)

Message = Union[Command, Event, ReturnMessage]
MessageType = TypeVar("MessageType", bound=Union[Command, Event, ReturnMessage])


LOG_LEVELS = ["debug", "info", "warning", "error", "disabled"]


@define
class MessageBus:
    """
    This is a basic implementation of Message Bus. Create a subclass of this if you
    need to change logging and/or exception handling.

    Usage:

    .. code-block:: python

        results = MessageBus(my_message)()

    If you're doing CQRS and/or don't use
    :py:class:`~messagebus.returnmessage.ReturnMessage` objects.

    .. code-block:: python

        MessageBus(my_message)()

    Alternatively, you can use :py:func:`~messagebus.handle_message`. It has the same
    arguments and return values. (It won't work if you have subclassed ``MessageBus``).
    """

    initial_message: Message = field()
    log_level: Literal["debug", "info", "disabled"] = field(
        default="info",
        kw_only=True,
        validator=in_(("debug", "info", "disabled")),
        metadata={"description": "The log level for non-error activity."},
    )
    error_log_level: Literal["info", "warning", "error", "disabled"] = field(
        default="error",
        kw_only=True,
        validator=in_(("info", "warning", "error", "disabled")),
        metadata={"description": "The log level for errors."},
    )

    return_messages: list[Any] = field(init=False)
    receiver_map: dict = field(init=False)
    handler_map: dict = field(init=False)
    _logger: Callable = field(init=False)
    _error_logger: Callable = field(init=False)

    def __attrs_post_init__(self):
        self.return_messages = []
        self.receiver_map = {}
        self.handler_map = defaultdict(list)
        self._logger = (
            getattr(logger, self.log_level) if self.log_level != "disabled" else None
        )
        self._error_logger = (
            getattr(logger, self.error_log_level)
            if self.error_log_level != "disabled"
            else None
        )

    @final
    def __call__(self) -> list[ReturnMessage]:
        self._process_message(self.initial_message)
        return self.return_messages

    def log_activity(self, *args):
        """
        Handles logging of actions to a standard Python logger. Override in a subclass
        for custom handling.
        """
        if self._logger:
            self._logger(*args)

    def log_error(self, msg: str, exc: Exception | None = None, **kwargs):
        """
        Logs an error including display of ``exc``. Any remaining keyword arguments
        are passed to the standard Python logger. Override in a subclass for custom
        handling.
        """
        if self._error_logger is not None:
            self._error_logger(msg, exc_info=exc, **kwargs)

    @final
    def _process_message(self, message: Message) -> Sequence[Message]:
        try:
            self.message_dispatcher(message)

        except Exception as exc:  # noqa: BLE001
            self.handle_exception(exc, message)

        return []

    def message_dispatcher(self, message: Message) -> None:
        """
        Override this in a subclass to add retry logic around the call to
        ``dispatch_message``. Otherwise, any exceptions that occur are raised
        immediately.

        Recommended: `tenacity`_

        .. _tenacity: https://tenacity.readthedocs.io/en/latest/index.html
        """
        self.dispatch_message(message)

    @final
    def dispatch_message(self, message: Message) -> None:
        match message:
            case Command():
                new_receiver_messages: ReceiverReturnType = self._execute_command(
                    message
                )
                for new_message in new_receiver_messages:
                    self._process_message(new_message)

            case Event():
                event: Event = message
                new_event_messages: HandlerReturnType = self._handle_event(event)
                for new_message in new_event_messages:
                    self._process_message(new_message)

            case ReturnMessage():
                if message not in self.return_messages:
                    self.return_messages.append(message)

            case _:
                raise UnknownMessageTypeError(type(message))

    def handle_exception(self, exc: Exception, message: Message) -> None:
        """
        Override this in a subclass to customize exception handling.

        A note from the book to keep in mind in your code:

        .. note::

            “Since we don’t know who’s handling an event, senders should not care
            whether the receivers succeeded or failed.”

        By default, exceptions raised will be logged and raised.
        """
        if self._error_logger is not None:
            self.log_error(
                f"An error occurred while processing message: {message}",
                exc,
            )

        raise exc

    @final
    def _execute_command(self, command: Command) -> list[Message]:
        self.log_activity(f"Executing command: {command!s}")
        receiver = self._get_receiver(command)
        note = f"No receiver found for command: {command!s}"
        if receiver is None:
            self.log_error(note)
            raise MessageBusConfigurationError(note)

        return receiver.execute_command()

    @final
    def _get_receiver(self, command: Command) -> Receiver | None:
        receiver_cls: type[Receiver] | None = self._get_receiver_cls(command)
        if receiver_cls is None:
            return None

        return receiver_cls(command=command)

    @final
    def _get_receiver_cls(self, command: Command) -> type[Receiver] | None:
        if command.__class__ in self.receiver_map:
            return self.receiver_map[command.__class__]

        receiver_cls: type[Receiver] | None
        for receiver_cls in Receiver.__subclasses__():
            if receiver_cls.handles_command(command):
                self.receiver_map[command.__class__] = receiver_cls
                return receiver_cls

        msg = f"No receiver found for command: {command!s}"
        raise MessageBusConfigurationError(msg)

    @final
    def _handle_event(self, event: Event) -> HandlerReturnType:
        self.log_activity(f"Handling event: {event!s}")
        handler_classes: list[type[Handler]] = self.get_event_handlers(event)

        if not handler_classes:
            msg = f"No handler found for event: {event!s}"
            raise MessageBusConfigurationError(msg)

        new_messages: HandlerReturnType = []
        handler_cls: HandlerType
        for handler_cls in handler_classes:
            handler = handler_cls(event)
            new_messages.extend(handler.handle_event())

        return new_messages

    @final
    def get_event_handlers(self, event: Event) -> list[type[Handler]]:
        if event.__class__ in self.handler_map:
            return self.handler_map[event.__class__]

        for handler_subclass in Handler.__subclasses__():
            handler_cls: HandlerType = handler_subclass
            self.register_matching_handler(event, handler_cls)

        return self.handler_map[event.__class__]

    def register_matching_handler(self, event: Event, handler_cls: HandlerType):
        """
        Register a handler class for the given event class.
        """
        if (
            type(event) in handler_cls.handles_events
            and handler_cls not in self.handler_map[event.__class__]
        ):
            self.handler_map[event.__class__].append(handler_cls)


def handle_message(
    message: Message,
    *,
    log_level: Literal["debug", "info", "disabled"] = "disabled",
    error_log_level: Literal["warning", "error", "disabled"] = "disabled",
):
    """
    Convenience function to process a message using
    :py:class:`~messagebus.messagebus.MessageBus`.

    Usage:

    .. code-block:: python

        return_messages = handle_message(my_message)

    If you're doing CQRS and/or don't use
    :py:class:`~messagebus.returnmessage.ReturnMessage` objects.

    .. code-block:: python

        handle_message(my_message)

    """
    return MessageBus(
        message,
        log_level=log_level,
        error_log_level=error_log_level,
    )()
