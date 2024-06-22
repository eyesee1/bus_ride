from abc import ABC, abstractmethod
from typing import ClassVar

from attrs import define, field

from . import MessageBusConfigurationError
from .command import Command
from .event import Event
from .returnmessage import ReturnMessage

type HandlerReturnType = list[Command | ReturnMessage]


@define
class Handler(ABC):
    """
    Abstract base class for handling one or more :py:class:`~messagebus.event.Event`.

    Event handlers should do as little as possible, such as send a quick notification,
    log an action, or issue Command(s). If an Event implies anything significant needs
    to be done in response, the Handler should return
    :py:class:`~messagebus.command.Command` object(s). We can't enforce this guideline
    for you, but recommend you follow it.

    Your handler may return a list containing :py:class:`~messagebus.command.Command`
    and/or :py:class:`~messagebus.returnmessage.ReturnMessage` objects.

    If one or more :py:class:`~messagebus.returnmessage.ReturnMessage` are returned,
    your application should do something with them.

    .. note::

        Event handlers are located by searching through all subclasses of
        ``Handler``, to find Handler(s) that accept the Event. They are cached once
        located. If any of your Handlers are not being used when they should be,
        make sure they are imported when your application starts up. Usually,
        importing them in an ``__init__.py`` file or keeping them in the same file
        with their ``Event`` will fix it.

    """

    event: Event = field()

    handles_events: ClassVar[list[type[Event]]]
    """
    A list of the :py:class:`~messagebus.event.Event` class(es) this ``Handler`` should
    respond to.
    """

    def __attrs_post_init__(self):  # pragma: no cover
        if not self.handles_events:
            msg = f"Handler {self.__class__.__name__} must define handles_events."
            raise MessageBusConfigurationError(msg)

    @abstractmethod
    def handle_event(self) -> HandlerReturnType:  # pragma: no cover
        """
        Your implementation of a response to ``self.event``.
        """
        raise NotImplementedError

    @classmethod
    def handles_event(cls, event: Event) -> bool:  # pragma: no cover
        """
        Determines whether this handler should respond to ``event``.
        """
        return type(event) in cls.handles_events


type HandlerType = type[Handler]
