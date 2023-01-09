from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from signal_ocean.tonnage_list import (
    Port,
    VesselClass,
    MarketDeployment,
    PushType,
    CommercialStatus,
    VesselSubclass,
    LocationTaxonomy,
    Area,
    Vessel,
)


def create_port(port_id: int = 1, name: str = "port name") -> Port:
    return Port(port_id, name)


def create_vessel_class(
    vessel_id: int = 1, name: str = "vessel class name"
) -> VesselClass:
    return VesselClass(vessel_id, name)


def create_vessel(
    imo: int = 123,
    name: str = "name",
    vessel_class: str = "Aframax",
    ice_class: Optional[str] = "ice class",
    year_built: int = 1990,
    deadweight: int = 200000,
    length_overall: float = 200.5,
    breadth_extreme: int = 50,
    market_deployment: str = MarketDeployment.SPOT,
    push_type: str = PushType.PUSHED,
    open_port_id: int = 123,
    open_port: str = "open port",
    open_date: Optional[datetime] = datetime.now(tz=timezone.utc)
    - timedelta(days=3),
    operational_status: str = "operational status",
    commercial_operator_id: int = 123,
    commercial_operator: str = "commercial operator",
    commercial_status: str = CommercialStatus.AVAILABLE,
    eta: Optional[datetime] = datetime.now(tz=timezone.utc)
    + timedelta(days=2),
    latest_ais: Optional[datetime] = datetime.now(tz=timezone.utc)
    - timedelta(days=2),
    subclass: str = VesselSubclass.DIRTY,
    willing_to_switch_subclass: bool = True,
    open_prediction_accuracy: str = LocationTaxonomy.PORT,
    open_areas: Tuple[Area, ...] = (
        Area(123, "country", LocationTaxonomy.COUNTRY, 0),
        Area(456, "narrow", LocationTaxonomy.NARROW_AREA, 1),
        Area(789, "wide", LocationTaxonomy.WIDE_AREA, 2),
    ),
    availability_port_type: str = "Prediction",
    availability_date_type: str = "Prediction",
    fixture_type: str = "fixture_type",
    current_vessel_sub_type_id: int = 123,
    current_vessel_sub_type: str = "current_vessel_sub_type",
    willing_to_switch_current_vessel_sub_type: bool = True,
) -> Vessel:
    return Vessel(
        imo,
        name,
        vessel_class,
        ice_class,
        year_built,
        deadweight,
        length_overall,
        breadth_extreme,
        market_deployment,
        push_type,
        open_port,
        open_port_id,
        open_date,
        operational_status,
        commercial_operator_id,
        commercial_operator,
        commercial_status,
        eta,
        latest_ais,
        subclass,
        willing_to_switch_subclass,
        open_prediction_accuracy,
        open_areas,
        availability_port_type,
        availability_date_type,
        fixture_type,
        current_vessel_sub_type_id,
        current_vessel_sub_type,
        willing_to_switch_current_vessel_sub_type
    )
