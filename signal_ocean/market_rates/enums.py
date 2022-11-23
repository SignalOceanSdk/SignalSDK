# noqa: D100

from enum import Enum, unique


@unique
class CargoId(Enum):
    """An enumeration of all possible cargo ids."""
    DIRTY = 0
    CLEAN = 1
    IMO = 2
