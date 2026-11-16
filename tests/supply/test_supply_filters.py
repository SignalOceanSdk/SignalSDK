from datetime import date, datetime

import pytest
from pydantic import ValidationError

from signal_ocean.supply.constants import (
    LocationTaxonomy,
    MarketStatus,
    VesselClass,
    VoyageState,
)
from signal_ocean.supply.filters import (
    AisTrackingFilter,
    CommercialAvailabilityFilter,
    EtaConfiguration,
    EtaConfigurationWithRestrictions,
    FromToRange,
    GeoLocation,
    IncludeExcludeFilter,
    LiveSupplyFilter,
    SupplyFilter,
    VesselParticularsFilter,
    VoyageDetailsFilter,
)

COMMERCIAL_AVAILABILITY_FILTER = [
    "openLocation", "openDate", "openDateRelativeOffset",
    "availabilityState", "marketStatus", "marketDeployment",
    "positionSourceOrigin", "positionSourceType", "lastMarketedDate",
    "lastMarketedDateRelativeOffset", "latestUpdatedDate",
    "latestUpdatedDateRelativeOffset", "forecastedDestination",
]
VOYAGE_DETAILS_FILTER = [
    "voyageState", "reportedLastCargoTypeId", "cargoTypeId",
    "lastVoyageCargoTypeId", "startPort", "cargoQuantity", "charterer",
]
AIS_TRACKING_FILTER = [
    "daysSinceLatestAis", "aisDraught", "aisHeading", "aisSpeed",
    "aisCurrentArea", "aisClosestLocation", "aisDestination",
    "etaToAisDestination",
]
VESSEL_PARTICULARS_FILTER = [
    "commercialOperator", "liquidCapacity", "iceClass", "cranesTonCapacity",
    "lengthOverall", "breadthExtreme", "airDraught",
    "ballastParallelBodyLength", "bowToCenterManifold", "classRenewalDate",
    "builtCountryCode", "builtCountryName", "crudeOilWashing",
    "deliveryDate", "flagCode", "heatingCoilsFitted", "inertGasSystem",
    "lightshipTonnes", "mainEngineManufacturerId", "mainEngineManufacturer",
    "mainEngineKw", "mainEngineRpm", "mouldedDepth", "parallelBodyLength",
    "reducedGrossTonnage", "shipyardBuiltId", "sternLine",
    "waterLineToManifold", "builtForTradeIds", "baleCapacity", "co2Fitted",
    "grainCapacity", "neoPanamaLocks", "numberOfHolds", "australianLadder",
    "logFitted", "openHatch", "a60Bulkhead", "grossRegisteredTonnage",
    "netRegisteredTonnage", "headOwnerId", "ballastWaterTreatment",
    "draught", "geared", "classificationRegisterId", "vesselAge", "coating",
    "imoType", "craneMaxOutReach", "craneLiftingCapacity", "numberOfCranes",
    "boxShapedHolds", "holdLength", "holdHeight", "holdBreadth",
    "numberOfHatches", "hasHatches", "hatchLength", "hatchBreadth",
    "numberOfGrabs", "hasGrabs", "grabLiftingCapacity",
    "grabMaxLiftingWeight", "scrubbers", "yearBuilt", "numberOfBowThrusters",
    "numberOfBowChainStoppers", "propulsionType", "gasContainmentType",
    "summerTpc", "designModel", "sanctionStatus", "trade",
]
ETA_CONFIGURATION = [
    "basisPortId", "speed", "seaMargin", "etaCalculationBasis", "eta",
    "etaRelativeOffset", "id",
]
ETA_CONFIGURATION_WITH_RESTRICTIONS = [
    "basisPortId", "speed", "seaMargin", "restrictions",
    "etaCalculationBasis", "eta", "etaRelativeOffset", "id",
]
SUPPLY_REQUEST_FILTERS = [
    "vesselClass", "vesselType", "size", "definingSize", "vesselSubclass",
    "addWillingToSwitchSubclass", "imo", "searchText",
    "commercialAvailability", "voyageDetails", "aisTracking",
    "etaConfiguration", "vesselParticulars",
]


def _dump(model):
    return model.model_dump(mode="json", by_alias=True, exclude_unset=True)


@pytest.mark.parametrize(
    "model, expected",
    [
        (CommercialAvailabilityFilter, COMMERCIAL_AVAILABILITY_FILTER),
        (VoyageDetailsFilter, VOYAGE_DETAILS_FILTER),
        (AisTrackingFilter, AIS_TRACKING_FILTER),
        (VesselParticularsFilter, VESSEL_PARTICULARS_FILTER),
        (EtaConfiguration, ETA_CONFIGURATION),
        (EtaConfigurationWithRestrictions,
         ETA_CONFIGURATION_WITH_RESTRICTIONS),
        (SupplyFilter, SUPPLY_REQUEST_FILTERS),
        (LiveSupplyFilter, SUPPLY_REQUEST_FILTERS),
    ],
)
def test_request_aliases_match_apim_contract(model, expected):
    aliases = {field.alias for field in model.model_fields.values()}

    assert aliases == set(expected)


def test_dump_is_camel_case_and_omits_unset():
    supply_filter = SupplyFilter(
        vessel_class="Aframax",
        commercial_availability=CommercialAvailabilityFilter(
            open_date_relative_offset=FromToRange(from_=-5, to=0)
        ),
    )

    assert _dump(supply_filter) == {
        "vesselClass": "Aframax",
        "commercialAvailability": {
            "openDateRelativeOffset": {"from": -5, "to": 0}
        },
    }


def test_unknown_field_raises():
    with pytest.raises(ValidationError):
        CommercialAvailabilityFilter(open_dat=FromToRange(from_=0, to=1))


def test_dates_dump_as_iso():
    supply_filter = CommercialAvailabilityFilter(
        open_date=FromToRange(
            from_=date(2026, 10, 1), to=datetime(2026, 10, 2, 12, 0)
        )
    )

    assert _dump(supply_filter) == {
        "openDate": {"from": "2026-10-01", "to": "2026-10-02T12:00:00"}
    }


def test_geo_location_in_include_exclude_dumps_camel_case():
    location_filter = IncludeExcludeFilter(
        excluded=[
            GeoLocation(geo_id=3853, location_taxonomy=LocationTaxonomy.PORT)
        ]
    )

    assert _dump(location_filter) == {
        "excluded": [{"geoId": 3853, "locationTaxonomy": 2}]
    }


def test_restrictions_only_on_live_filter():
    eta = [EtaConfigurationWithRestrictions(
        basis_port_id=3853, restrictions="Suez"
    )]

    live = LiveSupplyFilter(eta_configuration=eta)

    assert _dump(live) == {
        "etaConfiguration": [{"basisPortId": 3853, "restrictions": "Suez"}]
    }
    with pytest.raises(ValidationError):
        SupplyFilter(eta_configuration=eta)


def test_constants_values():
    assert VesselClass.PANAMAX_TANKER == "PanamaxTanker"
    assert VoyageState.BALLAST_UNFIXED == "BallastUnfixed"
    assert MarketStatus.POSS_PUSHED == "PossPushed"
    assert LocationTaxonomy.LEVEL0 == 4
