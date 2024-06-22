class Command:
    """
    Base class for all Commands.

    Subclass this and add the necessary fields to communicate the command to its
    :py:class:`~messagebus.receiver.Receiver`.

    Commands should simply carry data to their Receiver, they don't *do* anything.

    Using ``@define`` and ``field`` from attrs is recommended to keep it short.
    """
