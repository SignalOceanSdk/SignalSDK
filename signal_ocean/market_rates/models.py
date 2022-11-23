# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MarketRate:
    """The market rate of a certain route or vessel class.

    Attributes:
        route_id: ID of the route.
        rate_date: Date of the rate.
        rate_value: Value of the rate.
        unit: Unit of the rate.
        vessel_class_id: ID of the vessel class.
        deprecated_to: Route ID if route is deprecated.
    """

    route_id: str
    rate_date: datetime
    rate_value: float
    unit: str
    vessel_class_id: int
    deprecated_to: Optional[str] = None


@dataclass(frozen=True)
class Route:
    """A route with available market rate.

    Attributes:
        id: ID of the route.
        description: Description of the route.
        unit: Unit in which rate is provided.
        vessel_class_id: ID of the vessel class.
        cargo_id: Cargo ID.
        load_port_id: Load port ID.
        discharge_port_id: Discharge port ID.
        load_area_id: Load area ID.
        discharge_area_id: Discharge area ID.
        load_port_2_id: Second load port ID.
        discharge_port_2_id: Second discharge port ID.
        load_area_2_id: Second load area ID.
        discharge_area_2_id: Second discharge area ID.
        deprecated_to: Route ID if route is deprecated.
        deprecated_since: Deprecation effective date.
    """

    id: str
    description: str
    unit: str
    vessel_class_id: int
    cargo_id: int
    load_port_id: int
    discharge_port_id: int
    load_area_id: int
    discharge_area_id: int
    load_port_2_id: Optional[int] = None
    discharge_port_2_id: Optional[int] = None
    load_area_2_id: Optional[int] = None
    discharge_area_2_id: Optional[int] = None
    deprecated_to: Optional[str] = None
    deprecated_since: Optional[datetime] = None


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
