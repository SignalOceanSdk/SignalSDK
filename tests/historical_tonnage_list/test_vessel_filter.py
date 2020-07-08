from datetime import timedelta

from signal_ocean.historical_tonnage_list import VesselFilter


def test_converts_to_query_string():
    vessel_filter = VesselFilter(
        push_types=['pt1', 'pt2'],
        market_deployments=['md1', 'md2'],
        commercial_statuses=['cs1', 'cs2'],
        vessel_subclass='vsc',
        add_willing_to_switch_subclass=True,
        latest_ais_since=5,
        operational_statuses=['os1', 'os2']
    )

    query_string = vessel_filter.to_query_string()

    assert query_string == {
        'pushType': ['pt1', 'pt2'],
        'marketDeployment': ['md1', 'md2'],
        'commercialStatus': ['cs1', 'cs2'],
        'vesselSubclass': 'vsc',
        'addWillingToSwitchSubclass': True,
        'latestAisSince': 5,
        'operationalStatus': ['os1', 'os2']
    }

def test_converting_to_query_string_handles_missing_values():
    vessel_filter = VesselFilter(
        push_types=None,
        market_deployments=None,
        commercial_statuses=None,
        vessel_subclass=None,
        add_willing_to_switch_subclass=None,
        latest_ais_since=None,
        operational_statuses=None
    )

    query_string = vessel_filter.to_query_string()

    assert query_string == {
        'pushType': None,
        'marketDeployment': None,
        'commercialStatus': None,
        'vesselSubclass': None,
        'addWillingToSwitchSubclass': None,
        'latestAisSince': None,
        'operationalStatus': None
    }
