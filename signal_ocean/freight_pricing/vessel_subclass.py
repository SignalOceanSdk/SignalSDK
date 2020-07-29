# noqa: D100

from enum import Enum, unique


@unique
class VesselSubclass(Enum):
    """An enumeration of all possible vessel classes."""
    DIRTY = 1
    CLEAN = 2
