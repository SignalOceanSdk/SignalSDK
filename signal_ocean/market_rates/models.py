# noqa: D100

from typing import Optional

from signal_ocean.util.pydantic_base import SignalBaseModel, UTCDatetime


class MarketRate(SignalBaseModel):
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
    rate_date: UTCDatetime
    rate_value: float
    unit: str
    vessel_class_id: int
    deprecated_to: Optional[str] = None


class Route(SignalBaseModel):
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
    vessel_class_id: Optional[int] = None
    cargo_id: Optional[int] = None
    load_port_id: Optional[int] = None
    discharge_port_id: Optional[int] = None
    load_area_id: Optional[int] = None
    discharge_area_id: Optional[int] = None
    load_port_2_id: Optional[int] = None
    discharge_port_2_id: Optional[int] = None
    load_area_2_id: Optional[int] = None
    discharge_area_2_id: Optional[int] = None
    deprecated_to: Optional[str] = None
    deprecated_since: Optional[UTCDatetime] = None


class VesselClass(SignalBaseModel):
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
