# noqa: D100

from .._internals import IterableConstants


class VesselSubclass(metaclass=IterableConstants):
    """Contains constants for available vessel subclasses."""

    ALL = None
    DIRTY = 'Dirty'
    CLEAN = 'Clean'
