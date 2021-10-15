from datetime import datetime, timezone

from signal_ocean.tonnage_list import (
    _json,
    MarketDeployment,
    PushType,
    CommercialStatus,
    VesselSubclass,
)


def test_handles_empty_json_response() -> None:
    htl = _json.parse_historical_tonnage_list_response({})

    assert len(htl) == 0


def test_handles_missing_static_vessel_data() -> None:
    htl = _json.parse_historical_tonnage_list_response(
        {
            "tonnageLists": [
                {
                    "date": "2020-05-28T00:00:00Z",
                    "pointInTimeVesselData": [
                        {
                            "imo": 12345,
                            "marketDeployment": "Spot",
                            "pushType": "Not Pushed",
                            "openPort": "Hong Kong",
                            "openDate": "2019-06-20T00:00:00Z",
                            "operationalStatus": "Laden",
                            "commercialOperator": "Commercial Operator",
                            "commercialStatus": "Available",
                            "eta": "2019-07-15T00:00:00Z",
                            "latestAis": "2019-06-13T00:00:00Z",
                        }
                    ],
                }
            ],
            "staticVesselData": [],
        }
    )

    assert len(htl) == 1
    tonnage_list = htl[0]
    assert tonnage_list.date == datetime(
        year=2020, month=5, day=28, tzinfo=timezone.utc
    )

    assert len(tonnage_list.vessels) == 1
    vessel = tonnage_list.vessels[0]
    assert vessel.imo == 12345
    assert vessel.market_deployment == MarketDeployment.SPOT
    assert vessel.push_type == PushType.NOT_PUSHED
    assert vessel.open_port == "Hong Kong"
    assert vessel.open_date == datetime(
        year=2019, month=6, day=20, tzinfo=timezone.utc
    )
    assert vessel.operational_status == "Laden"
    assert vessel.commercial_operator == "Commercial Operator"
    assert vessel.commercial_status == CommercialStatus.AVAILABLE
    assert vessel.eta == datetime(
        year=2019, month=7, day=15, tzinfo=timezone.utc
    )
    assert vessel.latest_ais == datetime(
        year=2019, month=6, day=13, tzinfo=timezone.utc
    )
    assert vessel.name is None
    assert vessel.vessel_class is None
    assert vessel.ice_class is None
    assert vessel.year_built is None
    assert vessel.deadweight is None
    assert vessel.length_overall is None
    assert vessel.breadth_extreme is None
    assert vessel.subclass is None


def test_does_not_return_vessels_not_in_tonnage_lists() -> None:
    htl = _json.parse_historical_tonnage_list_response(
        {
            "tonnageLists": [],
            "staticVesselData": [
                {
                    "imo": 12345,
                    "vesselName": "Vessel Name",
                    "vesselClass": "Aframax",
                    "iceClass": None,
                    "yearBuilt": 1990,
                    "deadWeight": 113005,
                    "lengthOverall": 249.96,
                    "breadthExtreme": 44,
                    "subclass": "Product",
                }
            ],
        }
    )

    assert len(htl) == 0


def test_combines_static_and_point_in_time_vessel_data() -> None:
    imo = 12345
    htl = _json.parse_historical_tonnage_list_response(
        {
            "tonnageLists": [
                {
                    "date": "2020-05-28T00:00:00Z",
                    "pointInTimeVesselData": [
                        {
                            "imo": imo,
                            "marketDeployment": "Spot",
                            "pushType": "Not Pushed",
                            "openPort": "Hong Kong",
                            "openDate": "2019-06-20T00:00:00Z",
                            "operationalStatus": "Laden",
                            "commercialOperator": "Commercial Operator",
                            "commercialStatus": "Available",
                            "eta": "2019-07-15T00:00:00Z",
                            "latestAis": "2019-06-13T00:00:00Z",
                        }
                    ],
                }
            ],
            "staticVesselData": [
                {
                    "imo": imo,
                    "vesselName": "Vessel Name",
                    "vesselClass": "Aframax",
                    "iceClass": "1A",
                    "yearBuilt": 1990,
                    "deadWeight": 113005,
                    "lengthOverall": 249.96,
                    "breadthExtreme": 44,
                    "subclass": "Clean",
                }
            ],
        }
    )

    vessel = htl[0].vessels[0]
    assert vessel.imo == imo
    assert vessel.market_deployment == MarketDeployment.SPOT
    assert vessel.push_type == PushType.NOT_PUSHED
    assert vessel.open_port == "Hong Kong"
    assert vessel.open_date == datetime(
        year=2019, month=6, day=20, tzinfo=timezone.utc
    )
    assert vessel.operational_status == "Laden"
    assert vessel.commercial_operator == "Commercial Operator"
    assert vessel.commercial_status == CommercialStatus.AVAILABLE
    assert vessel.eta == datetime(
        year=2019, month=7, day=15, tzinfo=timezone.utc
    )
    assert vessel.latest_ais == datetime(
        year=2019, month=6, day=13, tzinfo=timezone.utc
    )
    assert vessel.name == "Vessel Name"
    assert vessel.vessel_class == "Aframax"
    assert vessel.ice_class == "1A"
    assert vessel.year_built == 1990
    assert vessel.deadweight == 113005
    assert vessel.length_overall == 249.96
    assert vessel.breadth_extreme == 44
    assert vessel.subclass == VesselSubclass.CLEAN


def test_handles_missing_values() -> None:
    imo = 12345
    htl = _json.parse_historical_tonnage_list_response(
        {
            "tonnageLists": [
                {
                    "date": "2020-05-28T00:00:00Z",
                    "pointInTimeVesselData": [{"imo": imo,}],
                }
            ],
            "staticVesselData": [{"imo": imo,}],
        }
    )

    vessel = htl[0].vessels[0]
    assert vessel.imo == imo
    assert vessel.market_deployment is None
    assert vessel.push_type is None
    assert vessel.open_port is None
    assert vessel.open_date is None
    assert vessel.operational_status is None
    assert vessel.commercial_operator is None
    assert vessel.commercial_status is None
    assert vessel.eta is None
    assert vessel.latest_ais is None
    assert vessel.name is None
    assert vessel.vessel_class is None
    assert vessel.ice_class is None
    assert vessel.year_built is None
    assert vessel.deadweight is None
    assert vessel.length_overall is None
    assert vessel.breadth_extreme is None
    assert vessel.subclass is None


def test_tolerates_unkown_values() -> None:
    imo = 12345
    htl = _json.parse_historical_tonnage_list_response(
        {
            "tonnageLists": [
                {
                    "date": "2020-05-28T00:00:00Z",
                    "pointInTimeVesselData": [
                        {
                            "imo": imo,
                            "marketDeployment": "unknown md",
                            "pushType": "unknown pt",
                            "operationalStatus": "unknown os",
                            "commercialStatus": "unknown cs",
                        }
                    ],
                }
            ],
            "staticVesselData": [{"imo": imo, "subclass": "unknown sc"}],
        }
    )

    vessel = htl[0].vessels[0]
    assert vessel.market_deployment == "unknown md"
    assert vessel.push_type == "unknown pt"
    assert vessel.operational_status == "unknown os"
    assert vessel.commercial_status == "unknown cs"
    assert vessel.subclass == "unknown sc"

