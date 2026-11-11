import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from signal_ocean.supply.models import (
    AisTracking,
    CommercialAvailability,
    SupplyEta,
    SupplyRecord,
    SupplySnapshot,
    SupplyTrend,
    VoyageDetails,
)

SAMPLE = Path(__file__).parent / "sample_supply_response.json"

COMMERCIAL_AVAILABILITY = [
    "openLocation", "openLocationTaxonomy", "openLocationGeoId",
    "openLocationTaxonomyId", "openDateFrom", "openDateTo",
    "availabilityState", "availabilityStateId", "marketStatus",
    "marketStatusId", "marketDeployment", "marketDeploymentId",
    "positionSourceOrigin", "positionSourceOriginId", "positionSourceType",
    "positionSourceTypeId", "lastMarketedDate", "latestUpdatedDate",
    "forecastedDestinationPort", "forecastedDestinationPortId",
]
VOYAGE_DETAILS = [
    "voyageState", "voyageStateId", "cargoType", "cargoTypeId",
    "cargoQuantity", "charterer", "chartererId", "startPort", "startPortId",
    "lastVoyageCargoTypes", "lastVoyageCargoTypeIds", "lastCargoTypes",
    "lastCargoTypeIds",
]
AIS_TRACKING = [
    "lastMovementDateTimeUTC", "daysSinceLatestAis", "aisLatitudeAverage",
    "aisLongitudeAverage", "aisDraughtAverage", "aisHeadingAverage",
    "aisSpeedAverage", "aisSeagoingSpeedAverage", "aisCurrentArea",
    "aisCurrentAreaId", "aisClosestLocation", "aisClosestLocationId",
    "aisDestination", "aisDestinationTaxonomy", "aisDestinationGeoId",
    "aisDestinationTaxonomyId", "etaToAisDestination",
    "milesToAisDestination", "delaysToAisDestination",
]
SUPPLY_ETA = ["basisPortId", "eta", "distance", "id", "canals"]
SUPPLY = [
    "day", "imo", "vesselClassId", "vesselClass", "commercialAvailability",
    "voyageDetails", "aisTracking", "etaDetails", "details",
]


def _sample():
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def test_parses_reference_sample():
    record = SupplySnapshot.model_validate(_sample()).data[0]

    assert record.imo == 9793997
    assert record.vessel_class == "Aframax"
    assert record.commercial_availability.open_location == "Houston"
    assert record.commercial_availability.availability_state == "Available"
    assert record.voyage_details.last_cargo_type_ids == (19, 16, 7)
    assert record.ais_tracking.last_movement_date_time_utc == datetime(
        2024, 1, 27, 9, 0, tzinfo=timezone.utc
    )
    assert record.eta_details == ()


@pytest.mark.parametrize(
    "model, expected",
    [
        (CommercialAvailability, COMMERCIAL_AVAILABILITY),
        (VoyageDetails, VOYAGE_DETAILS),
        (AisTracking, AIS_TRACKING),
        (SupplyEta, SUPPLY_ETA),
        (SupplyRecord, SUPPLY),
    ],
)
def test_response_aliases_match_apim_contract(model, expected):
    aliases = [field.alias for field in model.model_fields.values()]

    assert aliases == expected


def test_null_lists_become_empty():
    record = _sample()["data"][0]
    record["etaDetails"] = None

    assert SupplySnapshot.model_validate({"data": None}).data == ()
    trend = SupplyTrend.model_validate({"supplyPerDay": None, "notes": None})
    assert trend.supply_per_day == ()
    assert trend.notes == ()
    assert SupplyRecord.model_validate(record).eta_details == ()


def test_unknown_response_fields_are_ignored():
    record = _sample()["data"][0]
    record["vesselParticulars"] = {"operator": "x"}

    assert SupplyRecord.model_validate(record).imo == 9793997


def test_trend_parses_notes():
    trend = SupplyTrend.model_validate({
        "supplyPerDay": [{"date": "2026-10-01T00:00:00Z", "supply": 12}],
        "notes": ["n"],
    })

    assert trend.supply_per_day[0].supply == 12
    assert trend.notes == ("n",)
