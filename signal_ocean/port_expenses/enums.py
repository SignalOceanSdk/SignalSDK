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
class Canal(Enum):
    """An enumeration of all possible canals."""
    NONE = 0
    SUEZ = 1
    TURKISH = 2
    PANAMA = 3
    BALTIC = 4
    TORRES = 5
