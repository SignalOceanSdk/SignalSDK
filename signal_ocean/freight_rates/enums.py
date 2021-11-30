# noqa: D100

from enum import Enum, unique


@unique
class RateType(Enum):
    """An enumeration of all possible rate types."""
    WorldScale = 0
    LumpSum = 1
    PerMetricTone = 2


@unique
class RouteType(Enum):
    """An enumeration of all possible route types."""
    Unknown = 0
    Main = 1
    Secondary = 2


@unique
class VesselClass(Enum):
    """An enumeration of all vessel classes."""
    VLCC = 0
    Suezmax = 1
    Aframax = 2
    PanamaxTanker = 3
    MR2 = 4
    MR1 = 5
