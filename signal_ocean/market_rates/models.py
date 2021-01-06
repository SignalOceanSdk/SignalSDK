# noqa: D100

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketRate:
    """The market rate of a certain route or vessel class.

    Attributes:
        route_id: ID of the route.
        rate_date: Date of the rate.
        rate_value: Value of the rate.
        unit: Unit of the rate.
        vessel_class_id: ID of the vessel class.
    """

    route_id: str
    rate_date: datetime
    rate_value: float
    unit: str
    vessel_class_id: int


@dataclass(frozen=True)
class Route:
    """A route with available market rate.

    Attributes:
        id: ID of the route.
        description: Description of the route.
        unit: Unit in which rate is provided.
        vessel_class_id: ID of the vessel class.
        is_clean: True if cargo is clean.
    """

    id: str
    description: str
    unit: str
    vessel_class_id: int
    is_clean: bool


@dataclass(frozen=True)
class VesselClass:
    """A vessel class.

    Attributes:
        id: The vessel class id, e.g. 60 -> VLGC, 61 -> Midsize/LGC etc.
        vessel_type_id: The vessel type id, e.g. 6
        from_size: Minimum size
        to_size: Maximum size
        name: The vessel class name
        vessel_type: The vessel type name, e.g. LPG
        defining_size: Size type, e.g. CubicSize
        size: The vessel size, e.g. cbm
    """

    id: int
    vessel_type_id: int
    from_size: int
    to_size: int
    name: str
    vessel_type: str
    defining_size: str
    size: str
