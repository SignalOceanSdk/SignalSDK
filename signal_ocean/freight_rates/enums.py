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
    VLGC = 0
    MidsizeLGC = 1
    HandyLPG = 2
    SmallLPG = 3
    VLOC = 4
    Capesize = 5
    PostPanamaxDry = 6
    PanamaxDry = 7
    Supramax = 8
    Handymax = 9
    Handysize = 10
    ULVC = 11
    NewPanamax = 12
    PostPanamax = 13
    Panamax = 14
    Feedermax = 15
    Feeder = 16
    VLCC = 17
    Suezmax = 18
    Aframax = 19
    PanamaxTanker = 20
    MR2 = 21
    MR1 = 22
    SmallTanker = 23
    ModernTFTE = 24
    SmallDry = 25
    ULCC = 26
    SmallContainer = 27
