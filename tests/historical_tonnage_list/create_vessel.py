from datetime import datetime, timedelta, timezone

from signal_ocean.historical_tonnage_list import (
    Vessel,
    Area,
    LocationTaxonomy,
    MarketDeployment,
    PushType,
    CommercialStatus,
    VesselSubclass,
)


def create_vessel(
    imo=123,
    name="name",
    vessel_class="Aframax",
    ice_class="ice class",
    year_built=1990,
    deadweight=200000,
    length_overall=200.5,
    breadth_extreme=50,
    market_deployment=MarketDeployment.SPOT,
    push_type=PushType.PUSHED,
    open_port="open port",
    open_date=datetime.now(tz=timezone.utc) - timedelta(days=3),
    operational_status="operational status",
    commercial_operator="commercial operator",
    commercial_status=CommercialStatus.AVAILABLE,
    eta=datetime.now(tz=timezone.utc) + timedelta(days=2),
    latest_ais=datetime.now(tz=timezone.utc) - timedelta(days=2),
    subclass=VesselSubclass.DIRTY,
    willing_to_switch_subclass=True,
    open_prediction_accuracy=LocationTaxonomy.PORT,
    open_areas=(
        Area("country", LocationTaxonomy.COUNTRY),
        Area("narrow", LocationTaxonomy.NARROW_AREA),
        Area("wide", LocationTaxonomy.WIDE_AREA),
    ),
    availability_port_type="Prediction",
    availability_date_type="Prediction"
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
        open_date,
        operational_status,
        commercial_operator,
        commercial_status,
        eta,
        latest_ais,
        subclass,
        willing_to_switch_subclass,
        open_prediction_accuracy,
        open_areas,
        availability_port_type,
        availability_date_type
    )
