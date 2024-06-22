from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from attrs import define, field

from messagebus import Command, Event, MessageBusConfigurationError

if TYPE_CHECKING:
    from messagebus.returnmessage import ReturnMessage  # noqa: F401

type ReceiverReturnType = list[Command | Event | "ReturnMessage"]  # noqa: F821


@define
class Receiver(ABC):
    """
    Abstract base class for :py:class:`~messagebus.command.Command` implementations.

    .. note::

        Command receivers are located the first time a ``Command`` is used by searching
        through all subclasses of ``Receiver`` to find the one that accepts the command.
        It is cached after the first use.

    .. note::

        If any of your Receivers are not being used when they should be, make sure
        they are imported when your application starts up. Usually, importing them in
        an ``__init__.py`` file or keeping them in the same file with their ``Command``
        will fix it.

    """

    command: Command = field()

    handles_command_cls: ClassVar[type[Command]]
    """
    The :py:class:`~messagebus.command.Command` class this receiver should respond to.
    """

    def __attrs_post_init__(self):  # pragma: no cover
        if not self.handles_command_cls:
            note = (
                f"Receiver {self.__class__.__name__} must define handles_command_cls."
            )
            raise MessageBusConfigurationError(note)

    @abstractmethod
    def execute_command(self) -> ReceiverReturnType:  # pragma: no cover
        """
        Your code to execute the Command.
        """
        raise NotImplementedError

    @classmethod
    def handles_command(cls, command: Command) -> bool:
        """
        Determines whether the :py:class:`~messagebus.command.Command` may be executed
        by this :py:class:`~messagebus.receiver.Receiver`.
        """
        return type(command) is cls.handles_command_cls
