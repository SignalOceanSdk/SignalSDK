from datetime import datetime, timedelta, timezone

from signal_ocean.historical_tonnage_list import Vessel, OpenArea, LocationTaxonomy, \
    MarketDeployment, PushType, CommercialStatus, VesselSubclass


def create_vessel(
        imo=123,
        name='name',
        vessel_class='Aframax',
        ice_class='ice class',
        year_built=1990,
        deadweight=200000,
        length_overall=200.5,
        breadth_extreme=50,
        market_deployment=MarketDeployment.SPOT,
        push_type=PushType.PUSHED,
        open_port='open port',
        open_date=datetime.now(tz=timezone.utc) - timedelta(days=3),
        operational_status='operational status',
        commercial_operator='commercial operator',
        commercial_status=CommercialStatus.AVAILABLE,
        eta=datetime.now(tz=timezone.utc) + timedelta(days=2),
        last_fixed=4,
        latest_ais=datetime.now(tz=timezone.utc) - timedelta(days=2),
        subclass=VesselSubclass.DIRTY,
        willing_to_switch_subclass=True,
        open_prediction_accuracy=LocationTaxonomy.PORT,
        open_areas=(
            OpenArea('country', LocationTaxonomy.COUNTRY),
            OpenArea('narrow', LocationTaxonomy.NARROW_AREA),
            OpenArea('wide', LocationTaxonomy.WIDE_AREA)
        )) -> Vessel:
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
        last_fixed,
        latest_ais,
        subclass,
        willing_to_switch_subclass,
        open_prediction_accuracy,
        open_areas
    )
