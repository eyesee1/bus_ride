from attrs import define


@define
class Event:
    """
    Base class for Events.

    Add fields to your subclass, whatever is needed to communicate the event to your
    :py:class:`~messagebus.handler.Handler` class(es). An Event itself does not *do*
    anything but carry data to its Handler(s).

    Using ``@define`` and ``field`` from attrs is recommended to keep it short.
    """


EventType = type[Event]
