from typing import Any

from attrs import define, field


@define(frozen=True)
class ReturnMessage:
    """
    Use this to return arbitrary data to clients from a Receiver or Handler.

    .. note::

        Usage of this is considered an "ugly hack". Please see Chapter 12 of
        *Architecture Patterns with Python* to learn about
        *Command-Query Responsibility Segregation*
        (CQRS). ``ReturnMessage`` is here to support cases where you are not using CQRS.

    You can define any extra fields you want in a subclass, The message bus simply
    collects and returns these objects to the original caller.
    """

    data: Any = field()
