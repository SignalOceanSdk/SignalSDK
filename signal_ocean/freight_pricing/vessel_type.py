# noqa: D100

from enum import Enum, unique


@unique
class VesselType(Enum):
    """An enumeration of all possible vessel types."""
    TANKER = 1
