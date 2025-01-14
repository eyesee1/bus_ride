"""Tests for ``bus_ride`` package."""

from unittest import mock

import pytest

from bus_ride import MessageBus, handle_message
from bus_ride.exceptions import MessageBusConfigurationError

from .helpers import (
    FakeCommand,
    FakeCommand2,
    FakeCommandWithNoReceiver,
    FakeEvent,
    FakeEvent2,
    FakeEventWithNoHandler,
    FakeFailingCommand,
    FakeFailingEvent,
    FakeHandler,
    FakeReceiver,
    IntentionallyFailingTestError,
)


class TestMessageBus:
    base_helper_ref = "bus_ride.tests.helpers"

    def test_return_messages_get_returned(self):
        command = FakeCommand(what="Ice Cream Trucks", how_many=2)
        return_messages = MessageBus(command)()
        assert len(return_messages) == 1

    def test_failing_receiver(self):
        command = FakeFailingCommand(what="Ice Cream Trucks", how_many=2)
        with pytest.raises(IntentionallyFailingTestError):
            MessageBus(command)()

    def test_failing_handler(self):
        event = FakeFailingEvent(data="This better not work!")
        with pytest.raises(IntentionallyFailingTestError):
            MessageBus(event)()

    def test_correct_receivers_run(self):
        command = FakeCommand2(what="Pizzas", how_many=2)
        with (
            mock.patch(
                f"{self.base_helper_ref}.FakeReceiver.execute_command"
            ) as mock_wrong_receiver,
            mock.patch(
                f"{self.base_helper_ref}.FakeReceiver2.execute_command"
            ) as mock_correct_receiver,
        ):
            MessageBus(command)()

        mock_correct_receiver.assert_called_once()
        mock_wrong_receiver.assert_not_called()

    def test_correct_handlers_run(self):
        event = FakeEvent2(data="hello")
        with (
            mock.patch(
                f"{self.base_helper_ref}.FakeHandler.handle_event"
            ) as mock_wrong_handler,
            mock.patch(
                f"{self.base_helper_ref}.FakeHandler2.handle_event"
            ) as mock_correct_handler,
        ):
            MessageBus(event)()

        mock_wrong_handler.assert_not_called()
        mock_correct_handler.assert_called_once()

    def test_commands_event_runs(self):
        command = FakeCommand2(what="Dabs", how_many=2)
        with (
            mock.patch(
                f"{self.base_helper_ref}.FakeHandler.handle_event"
            ) as mock_wrong_handler,
            mock.patch(
                f"{self.base_helper_ref}.FakeHandler2.handle_event"
            ) as mock_correct_handler,
        ):
            MessageBus(command)()

        mock_wrong_handler.assert_not_called()
        mock_correct_handler.assert_called_once()

    def test_command_receiver_caching(self):
        command = FakeCommand(what="Pizzas", how_many=2)
        message_bus = MessageBus(command)
        message_bus()
        assert message_bus.receiver_map[FakeCommand] is FakeReceiver

    def test_event_handler_caching(self):
        event = FakeEvent(data="hello")
        message_bus = MessageBus(event)
        message_bus()
        handlers = message_bus.handler_map[FakeEvent]
        assert FakeHandler in handlers
        assert len(handlers) == 1

    def test_handle_message(self):
        command = FakeCommand(what="Ice Cream Trucks", how_many=2)
        with mock.patch(
            f"{self.base_helper_ref}.FakeReceiver.execute_command"
        ) as mock_receiver:
            handle_message(command)

        mock_receiver.assert_called_once()

        with mock.patch(
            f"{self.base_helper_ref}.FakeHandler.handle_event"
        ) as mock_handler:
            handle_message(command)

        mock_handler.assert_called_once()

    def test_get_receiver_for_command_with_no_receiver(self):
        command = FakeCommandWithNoReceiver(data=42)
        message_bus = MessageBus(command)

        with pytest.raises(MessageBusConfigurationError):
            message_bus._get_receiver_cls(command)

    def test_for_command_with_no_receiver(self):
        command = FakeCommandWithNoReceiver(data=42)
        message_bus = MessageBus(command)

        with pytest.raises(MessageBusConfigurationError):
            message_bus()

    def test_event_with_no_handler(self):
        event = FakeEventWithNoHandler(data="hello")

        with pytest.raises(MessageBusConfigurationError):
            MessageBus(event)()
