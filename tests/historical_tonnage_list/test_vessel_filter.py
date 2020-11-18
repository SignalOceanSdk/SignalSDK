from datetime import timedelta

from signal_ocean.historical_tonnage_list import VesselFilter
from datetime import date

def test_converts_to_query_string():
    vessel_filter = VesselFilter(
        push_types=['pt1', 'pt2'],
        market_deployments=['md1', 'md2'],
        commercial_statuses=['cs1', 'cs2'],
        vessel_subclass='vsc',
        add_willing_to_switch_subclass=True,
        latest_ais_since=5,
        operational_statuses=['os1', 'os2'],
        min_liquid_capacity=10,
        max_liquid_capacity=20,
        fixture_types=['ft1', 'ft2'],
        past_port_visits=[3300],
        open_port_ids=[3300],
        canakkale_cancelling=date(2020,10,10),
        open_date=date(2020,10,10),
        ice_classes=['1A'],
        min_cranes_ton_capacity=10,
        max_cranes_ton_capacity=20,
        min_length_overall=10,
        max_length_overall=20,
        min_breadth_extreme=10,
        max_breadth_extreme=20,
        open_area_ids=[24666],
        open_country_ids=[165]      
    )

    query_string = vessel_filter._to_query_string()

    assert query_string == {
        'pushType': ['pt1', 'pt2'],
        'marketDeployment': ['md1', 'md2'],
        'commercialStatus': ['cs1', 'cs2'],
        'vesselSubclass': 'vsc',
        'addWillingToSwitchSubclass': True,
        'latestAisSince': 5,
        'operationalStatus': ['os1', 'os2'],
        'minLiquidCapacity': 10,
        'maxLiquidCapacity': 20,
        'fixtureType': ['ft1', 'ft2'],
        "pastPortVisit": [3300],
        "openPortId": [3300],
        "canakkaleCancelling": '2020-10-10',
        "openDate": '2020-10-10',
        "iceClass": ['1A'],
        "cranesTonCapacityMin": 10,
        "cranesTonCapacityMax": 20,
        "lengthOverallMin": 10,
        "lengthOverallMax": 20,
        "breadthExtremeMin": 10,
        "breadthExtremeMax": 20,
        "openArea": [24666],
        "openCountry": [165]
    }

def test_converting_to_query_string_handles_missing_values():
    vessel_filter = VesselFilter(
        push_types=None,
        market_deployments=None,
        commercial_statuses=None,
        vessel_subclass=None,
        add_willing_to_switch_subclass=None,
        latest_ais_since=None,
        operational_statuses=None,
        min_liquid_capacity=None,
        max_liquid_capacity=None,
        fixture_types=None,
        past_port_visits=None,
        open_port_ids=None,
        canakkale_cancelling=None,
        open_date=None,
        ice_classes=None,
        min_cranes_ton_capacity=None,
        max_cranes_ton_capacity=None,
        min_length_overall=None,
        max_length_overall=None,
        min_breadth_extreme=None,
        max_breadth_extreme=None,
        open_area_ids=None,
        open_country_ids=None
        )

    query_string = vessel_filter._to_query_string()

    assert query_string == {
        'pushType': None,
        'marketDeployment': None,
        'commercialStatus': None,
        'vesselSubclass': None,
        'addWillingToSwitchSubclass': None,
        'latestAisSince': None,
        'operationalStatus': None,
        'minLiquidCapacity': None,
        'maxLiquidCapacity': None,
        'fixtureType': None,
        'pastPortVisit': None,
        'openPortId': None,
        'canakkaleCancelling': None,
        'openDate': None,
        'iceClass': None,
        'cranesTonCapacityMin': None,
        'cranesTonCapacityMax': None,
        'lengthOverallMin': None,
        'lengthOverallMax': None,
        'breadthExtremeMin': None,
        'breadthExtremeMax': None,
        'openArea': None,
        'openCountry': None
    }
