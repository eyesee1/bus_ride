class MessageBusError(Exception):
    """
    Base exception class for all message bus errors.
    """


class UnknownMessageTypeError(MessageBusError):
    """
    Raised when an unknown message type is passed to the message bus.
    """


class MessageBusConfigurationError(MessageBusError):
    """
    Raised when a configuration error is found, such as a command with no receiver.
    """
