# noqa: D100

from enum import Enum, unique


@unique
class Operation(Enum):
    """An enumeration of all possible operations."""
    LOAD = 0
    DISCHARGE = 1


@unique
class OperationStatus(Enum):
    """An enumeration of all possible operations statuses."""
    BALLAST = 0
    LADEN = 1


@unique
class ItalianAnchorageDues(Enum):
    """An enumeration of all possible italian anchorage dues."""
    NONE = 0
    MONTHLY = 1
    YEARLY = 2


@unique
class EstimationStatus(Enum):
    """An enumeration of all possible estimation statuses."""
    PRIORITY_TO_FORMULAS = 0
    PRIORITY_TO_ESTIMATES = 1
    NO_ESTIMATES = 2


@unique
class VesselTypeEnum(Enum):
    """An enumeration of all vessel types."""
    Tanker = 1
    Dry = 3
    Container = 4
    LNG = 5
    LPG = 6
