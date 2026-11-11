import copy
import inspect
import re
from datetime import date

import pytest

from signal_ocean.supply import templates
from signal_ocean.supply.filters import (
    CommercialAvailabilityFilter,
    EtaConfiguration,
    FromToRange,
    MinMaxRange,
    SupplyFilter,
    VesselParticularsFilter,
)
from signal_ocean.supply.templates import (
    build_filter_body,
    find_template,
    get_supply_templates,
)


def _geo(taxonomy, ids):
    return [{"geoId": i, "locationTaxonomy": taxonomy} for i in ids]


def level0(*ids):
    return _geo(4, ids)


def countries(*ids):
    return _geo(3, ids)


def ports(*ids):
    return _geo(2, ids)


TD3C_BODY = {
    "vesselType": "Tanker",
    "size": {"from": 200000, "to": 549999},
    "definingSize": "Deadweight",
    "vesselSubclass": ["Crude"],
    "commercialAvailability": {
        "openLocation": {
            "excluded": level0(
                24719, 24739, 24741, 24776, 24772, 25007, 24709
            )
        },
        "availabilityState": ["Available", "Cancelled", "Failed"],
        "marketStatus": {"values": ["Pushed", "PossPushed"]},
        "marketDeployment": ["Spot", "Relet"],
    },
    "aisTracking": {
        "aisDestination": {
            "excluded": level0(
                24767, 24772, 24776, 24746, 24676, 24733, 24671, 24600
            )
        }
    },
    "etaConfiguration": [{
        "id": "TD3C", "basisPortId": 3153,
        "etaCalculationBasis": "EarliestOpenDate",
        "speed": 13.0, "seaMargin": 0.0,
        "etaRelativeOffset": {"min": 0, "max": 18},
    }],
    "vesselParticulars": {
        "vesselAge": {"max": 15}, "sanctionStatus": {"values": [0]}
    },
}

P6_BODY = {
    "vesselType": "Dry",
    "size": {"from": 67000, "to": 84999},
    "definingSize": "Deadweight",
    "voyageDetails": {"voyageState": ["BallastFixed", "BallastUnfixed"]},
    "aisTracking": {
        "daysSinceLatestAis": 5,
        "aisHeading": [
            {"start": 157.5, "end": 202.5}, {"start": 202.5, "end": 247.5},
            {"start": 247.5, "end": 292.5}, {"start": 292.5, "end": 337.5},
        ],
        "aisSpeed": {"from": 3.0, "to": 30.0},
        "aisCurrentArea": {"values": [
            24769, 24767, 24772, 24776, 24779, 24771, 24702, 24655,
            24770, 24728, 24725, 24729, 24715, 24666, 24726, 24730,
        ]},
        "aisDestination": {"excluded": (
            ports(3248, 9079, 3253, 9076, 3244, 3235, 13013, 3241)
            + countries(20, 108, 210, 56, 55, 129)
            + level0(24772, 24737, 24778, 24583, 24584, 24738, 24712,
                     25007, 24709, 24758, 24757, 24594, 24755, 24756,
                     24673)
        )},
    },
    "etaConfiguration": [{
        "id": "P6", "basisPortId": 3245,
        "etaCalculationBasis": "LatestAisLocation",
        "speed": 13.0, "seaMargin": 0.0,
        "etaRelativeOffset": {"min": 0, "max": 40},
    }],
    "vesselParticulars": {"vesselAge": {"max": 20}},
}

HS4_BODY = {
    "vesselClass": "Handysize",
    "commercialAvailability": {
        "openLocation": {
            "values": level0(24676, 24733, 24600, 24671, 24746)
        },
        "openDateRelativeOffset": {"from": 0, "to": 10},
        "latestUpdatedDateRelativeOffset": {"from": -5, "to": 0},
    },
    "vesselParticulars": {"vesselAge": {"max": 20}},
}

ROUTE_CODES = (
    "TD1", "TD3C", "TD15", "TD23", "TD20", "TD6", "TD25", "TD19", "TD7",
    "TD8", "TC14", "TC2", "TC12", "TC6", "TC1", "TC5", "C3", "C5", "C7",
    "P6", "P1", "P3", "P5", "S5", "S2", "S10", "HS4", "HS5",
)

DATE_PAIRS = (
    ("openDate", "openDateRelativeOffset"),
    ("lastMarketedDate", "lastMarketedDateRelativeOffset"),
    ("latestUpdatedDate", "latestUpdatedDateRelativeOffset"),
)


def _template_body(code, filters=None):
    return build_filter_body(find_template(code), filters)


@pytest.mark.parametrize(
    "code, expected",
    [("TD3C", TD3C_BODY), ("P6", P6_BODY), ("HS4", HS4_BODY)],
)
def test_body_matches_template_definition(code, expected):
    assert _template_body(code) == expected


def test_template_codes():
    assert tuple(t.code for t in get_supply_templates()) == ROUTE_CODES


@pytest.mark.parametrize("template", get_supply_templates())
def test_every_template_is_well_formed(template):
    body = build_filter_body(template, None)
    size_band = [k for k in ("vesselType", "definingSize", "size")
                 if k in body]
    commercial = body.get("commercialAvailability", {})

    assert ("vesselClass" in body) != (len(size_band) == 3)
    assert "vesselClass" not in body or not size_band
    for absolute, relative in DATE_PAIRS:
        assert not (absolute in commercial and relative in commercial)
    for eta in body.get("etaConfiguration", []):
        assert not ("eta" in eta and "etaRelativeOffset" in eta)
        assert eta["id"] == template.code
    assert template.segment in ("Tanker", "Dry")


@pytest.mark.parametrize("template", get_supply_templates())
def test_no_tool_default_filters(template):
    body = build_filter_body(template, None)
    particulars = body.get("vesselParticulars", {})

    if template.segment == "Tanker":
        assert "daysSinceLatestAis" not in body.get("aisTracking", {})
        assert particulars["sanctionStatus"] == {"values": [0]}
    else:
        assert "sanctionStatus" not in particulars


def test_templates_source_has_no_guid():
    source = inspect.getsource(templates)

    guid = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    assert re.search(guid, source) is None


def test_lookup_ignores_case_and_spaces():
    assert find_template(" td3c ").code == "TD3C"


def test_unknown_code_lists_valid_codes():
    with pytest.raises(ValueError) as error:
        find_template("XX1")

    message = str(error.value)
    assert "XX1" in message
    assert "TD3C" in message
    assert "HS5" in message


def test_user_field_replaces_only_that_field():
    body = _template_body("TD3C", SupplyFilter(
        commercial_availability=CommercialAvailabilityFilter(
            availability_state=["Available"]
        )
    ))

    assert body["commercialAvailability"] == {
        **TD3C_BODY["commercialAvailability"],
        "availabilityState": ["Available"],
    }


def test_user_list_replaces_template_list():
    mine = EtaConfiguration(
        id="mine",
        basis_port_id=3853,
        eta_relative_offset=MinMaxRange(min=0, max=5),
    )

    body = _template_body("TD3C", SupplyFilter(eta_configuration=[mine]))

    assert body["etaConfiguration"] == [{
        "id": "mine",
        "basisPortId": 3853,
        "etaRelativeOffset": {"min": 0, "max": 5},
    }]


def test_explicit_none_removes_template_filter():
    body = _template_body("TD3C", SupplyFilter(
        vessel_particulars=VesselParticularsFilter(vessel_age=None)
    ))

    assert body["vesselParticulars"] == {"sanctionStatus": {"values": [0]}}


def test_user_vessel_class_drops_template_size_band():
    body = _template_body("TD3C", SupplyFilter(vessel_class="VLCC"))

    assert body["vesselClass"] == "VLCC"
    for key in ("vesselType", "size", "definingSize"):
        assert key not in body


def test_user_size_drops_template_vessel_class():
    body = _template_body("HS4", SupplyFilter(
        vessel_type="Dry",
        defining_size="Deadweight",
        size=FromToRange(from_=20000, to=30000),
    ))

    assert "vesselClass" not in body
    assert body["size"] == {"from": 20000, "to": 30000}


def test_user_absolute_date_drops_template_offset():
    body = _template_body("HS4", SupplyFilter(
        commercial_availability=CommercialAvailabilityFilter(
            open_date=FromToRange(
                from_=date(2026, 11, 1), to=date(2026, 11, 5)
            )
        )
    ))

    commercial = body["commercialAvailability"]
    assert commercial["openDate"] == {"from": "2026-11-01", "to": "2026-11-05"}
    assert "openDateRelativeOffset" not in commercial
    assert commercial["latestUpdatedDateRelativeOffset"] == {
        "from": -5, "to": 0
    }


def test_no_template_sends_only_user_fields():
    body = build_filter_body(
        None, SupplyFilter(vessel_class="Aframax", search_text=None)
    )

    assert body == {"vesselClass": "Aframax"}


def test_merge_does_not_change_stored_template():
    before = copy.deepcopy(_template_body("TD3C"))

    _template_body("TD3C", SupplyFilter(vessel_class="VLCC"))
    _template_body("TD3C", SupplyFilter(
        vessel_particulars=VesselParticularsFilter(vessel_age=None)
    ))

    assert _template_body("TD3C") == before == TD3C_BODY
