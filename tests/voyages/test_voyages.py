import dataclasses
from copy import copy
from datetime import datetime, date, timezone
from typing import Tuple, Dict, Union, List
from unittest.mock import MagicMock
from urllib.parse import urljoin

import pytest

from signal_ocean import Connection
from signal_ocean.voyages.models import Voyage, \
    VoyageEvent, VoyageEventDetail, VoyageGeo, VoyagesFlat, \
    VoyagesFlatPagedResponse
from signal_ocean.voyages.voyages_api import VoyagesAPI

_mock_flat_voyage_data_1 = {
    'ID': '91022.126',
    'IMO': 91022,
    'VoyageNumber': 126,
    'VesselName': 'Signal Vessel',
    'VesselTypeID': 1,
    'VesselType': 'Tanker',
    'VesselClassID': 84,
    'VesselClass': 'VLCC',
    'TradeID': 1,
    'Trade': 'Crude',
    'VesselStatusID': 1,
    'VesselStatus': 'Voyage',
    'CommercialOperatorID': 1028,
    'CommercialOperator': 'Signal',
    'StartDate': '2020-07-05T07:12:52Z',
    'EndDate': '2020-09-02T23:59:59Z',
    'CargoTypeID': 132000,
    'CargoType': 'Crude',
    'CargoGroupID': 130000,
    'CargoGroup': 'Dirty',
    'CargoTypeSource': 'Estimated'
}

_mock_flat_voyage_1 = Voyage(
    id='91022.126', imo=91022, voyage_number=126,
    vessel_name='Signal Vessel', vessel_type_id=1,
    vessel_type='Tanker', vessel_class_id=84,
    vessel_class='VLCC', trade_id=1, trade='Crude',
    vessel_status_id=1, vessel_status='Voyage',
    commercial_operator_id=1028,
    commercial_operator='Signal',
    start_date=datetime.fromisoformat(
        '2020-07-05T07:12:52'
    ).replace(tzinfo=timezone.utc),
    end_date=datetime.fromisoformat(
        '2020-09-02T23:59:59'
    ).replace(tzinfo=timezone.utc),
    cargo_type_id=132000, cargo_type='Crude',
    cargo_group_id=130000,
    cargo_group='Dirty',
    cargo_type_source='Estimated'
)

_mock_flat_voyage_data_2 = {
    'ID': '91022.173',
    'IMO': 91022,
    'VoyageNumber': 173,
    'VesselName': 'SII',
    'VesselTypeID': 1,
    'VesselType': 'Tanker',
    'VesselClassID': 84,
    'VesselClass': 'VLCC',
    'TradeID': 1,
    'Trade': 'Crude',
    'VesselStatusID': 1,
    'VesselStatus': 'Voyage',
    'CommercialOperatorID': 1028,
    'CommercialOperator': 'Signal',
    'StartDate': '2020-08-31T07:53:01Z',
    'EndDate': '2020-09-22T15:56:34.96Z',
    'CargoTypeID': 132000,
    'CargoType': 'Crude',
    'CargoGroupID': 130000,
    'CargoGroup': 'Dirty',
    'CargoTypeSource': 'Estimated'
}

_mock_flat_voyage_2 = Voyage(
    id='91022.173', imo=91022, voyage_number=173,
    vessel_name='SII', vessel_type_id=1,
    vessel_type='Tanker', vessel_class_id=84,
    vessel_class='VLCC', trade_id=1, trade='Crude',
    vessel_status_id=1, vessel_status='Voyage',
    commercial_operator_id=1028,
    commercial_operator='Signal',
    start_date=datetime.fromisoformat(
        '2020-08-31T07:53:01'
    ).replace(tzinfo=timezone.utc),
    end_date=datetime.fromisoformat(
        '2020-09-22T15:56:34.960'
    ).replace(tzinfo=timezone.utc),
    cargo_type_id=132000,
    cargo_type='Crude', cargo_group_id=130000,
    cargo_group='Dirty',
    cargo_type_source='Estimated'
)

_mock_event_data_1 = {
    'ID': '9102241.126.0',
    'VoyageID': '9102241.126',
    'EventType': 'Stop',
    'EventHorizon': 'Historical',
    'Purpose': 'Stop',
    'ArrivalDate': '2020-07-14T12:52:02Z',
    'SailingDate': '2020-07-15T21:12:48Z',
    'Latitude': 22.4618,
    'Longitude': 120.28313,
    'GeoAssetID': 5389,
    'GeoAssetName': 'Kaohsiung SPM',
    'PortID': 3821,
    'PortName': 'Kaohsiung'
}

_mock_event_1 = VoyageEvent(
    id='9102241.126.0', voyage_id='9102241.126',
    event_type='Stop', event_horizon='Historical',
    purpose='Stop',
    arrival_date=datetime.fromisoformat(
        '2020-07-14T12:52:02').replace(
        tzinfo=timezone.utc),
    sailing_date=datetime.fromisoformat(
        '2020-07-15T21:12:48').replace(
        tzinfo=timezone.utc), latitude=22.4618,
    longitude=120.28313, geo_asset_id=5389,
    geo_asset_name='Kaohsiung SPM', port_id=3821,
    port_name='Kaohsiung'
)

_mock_event_data_2 = {
    'ID': '9102241.126.1',
    'VoyageID': '9102241.126',
    'EventType': 'PortCall',
    'EventHorizon': 'Historical',
    'Purpose': 'Load',
    'ArrivalDate': '2020-07-20T07:59:02Z',
    'SailingDate': '2020-08-15T11:57:42Z',
    'Latitude': 1.27225,
    'Longitude': 103.97495,
    'GeoAssetID': 4446,
    'GeoAssetName': 'Changi Lightering Zone',
    'PortID': 3794,
    'PortName': 'Singapore',
    'LowAisDensity': True
}

_mock_event_2 = VoyageEvent(
    id='9102241.126.1', voyage_id='9102241.126',
    event_type='PortCall', event_horizon='Historical',
    purpose='Load',
    arrival_date=datetime.fromisoformat(
        '2020-07-20T07:59:02').replace(
        tzinfo=timezone.utc),
    sailing_date=datetime.fromisoformat(
        '2020-08-15T11:57:42').replace(
        tzinfo=timezone.utc),
    latitude=1.27225, longitude=103.97495,
    geo_asset_id=4446,
    geo_asset_name='Changi Lightering Zone',
    port_id=3794, port_name='Singapore',
    low_ais_density=True
)

_mock_event_detail_data_1 = {
    'EventDetailType': 'Stop',
    'ID': '9102241.126.0.0',
    'EventID': '9102241.126.0',
    'ArrivalDate': '2020-07-14T12:52:02Z',
    'SailingDate': '2020-07-15T21:12:48Z',
    'GeoAssetID': 5389,
    'GeoAssetName': 'Kaohsiung SPM',
    'Latitude': 22.4618,
    'Longitude': 120.28313
}

_mock_event_detail_1 = VoyageEventDetail(
    event_detail_type='Stop',
    id='9102241.126.0.0',
    event_id='9102241.126.0',
    arrival_date=datetime.fromisoformat(
        '2020-07-14T12:52:02'
    ).replace(tzinfo=timezone.utc),
    sailing_date=datetime.fromisoformat(
        '2020-07-15T21:12:48'
    ).replace(tzinfo=timezone.utc),
    geo_asset_id=5389,
    geo_asset_name='Kaohsiung SPM',
    latitude=22.4618, longitude=120.28313
)

_mock_event_detail_data_2 = {
    'EventDetailType': 'StS',
    'ID': '9102241.126.1.0',
    'EventID': '9102241.126.1',
    'ArrivalDate': '2020-07-20T07:59:02Z',
    'SailingDate': '2020-08-15T11:57:42Z',
    'StartTimeOfOperation': '2020-08-11T22:05:40Z',
    'EndTimeOfOperation': '2020-08-14T15:58:45Z',
    'GeoAssetID': 4446,
    'GeoAssetName': 'Lightering Zone',
    'Latitude': 1.27225,
    'Longitude': 103.97495,
    'OtherVesselIMO': 9183348,
    'OtherVesselName': 'Tian Ma Zuo'
}

_mock_event_detail_2 = VoyageEventDetail(
    event_detail_type='StS',
    id='9102241.126.1.0',
    event_id='9102241.126.1',
    arrival_date=datetime.fromisoformat(
        '2020-07-20T07:59:02').replace(tzinfo=timezone.utc),
    sailing_date=datetime.fromisoformat(
        '2020-08-15T11:57:42').replace(tzinfo=timezone.utc),
    start_time_of_operation=datetime.fromisoformat(
        '2020-08-11T22:05:40').replace(tzinfo=timezone.utc),
    end_time_of_operation=datetime.fromisoformat(
        '2020-08-14T15:58:45').replace(tzinfo=timezone.utc),
    geo_asset_id=4446,
    geo_asset_name='Lightering Zone',
    latitude=1.27225, longitude=103.97495,
    other_vessel_imo=9183348,
    other_vessel_name='Tian Ma Zuo'
)

_mock_geo_data_1 = {
    'ID': 5389,
    'Name': 'Kaohsiung SPM',
    'PortID': 3821,
    'PortName': 'Kaohsiung',
    'CountryID': 235,
    'Country': 'Taiwan',
    'AreaIDLevel0': 24729,
    'AreaNameLevel0': 'Taiwan',
    'AreaIDLevel1': 17,
    'AreaNameLevel1': 'China / Taiwan',
    'AreaIDLevel2': 99,
    'AreaNameLevel2': 'Far East',
    'AreaIDLevel3': 84,
    'AreaNameLevel3': 'East'
}

_mock_geo_1 = VoyageGeo(
    id=5389, name='Kaohsiung SPM', port_id=3821,
    port_name='Kaohsiung', country_id=235,
    country='Taiwan',
    area_idlevel0=24729, area_name_level0='Taiwan',
    area_idlevel1=17, area_name_level1='China / Taiwan',
    area_idlevel2=99, area_name_level2='Far East',
    area_idlevel3=84, area_name_level3='East'
)

_mock_geo_data_2 = {
    'ID': 4446,
    'Name': 'Changi Lightering Zone',
    'PortID': 3794,
    'PortName': 'Singapore',
    'CountryID': 205,
    'Country': 'Singapore',
    'AreaIDLevel0': 24655,
    'AreaNameLevel0': 'Singapore / Malaysia',
    'AreaIDLevel1': 23,
    'AreaNameLevel1': 'South East Asia',
    'AreaIDLevel2': 99,
    'AreaNameLevel2': 'Far East',
    'AreaIDLevel3': 84,
    'AreaNameLevel3': 'East'
}

_mock_geo_2 = VoyageGeo(
    id=4446, name='Changi Lightering Zone', port_id=3794,
    port_name='Singapore', country_id=205,
    country='Singapore', area_idlevel0=24655,
    area_name_level0='Singapore / Malaysia',
    area_idlevel1=23, area_name_level1='South East Asia',
    area_idlevel2=99, area_name_level2='Far East',
    area_idlevel3=84, area_name_level3='East'
)

_mock_flat_voyages_data_1 = {
    'Voyages': [_mock_flat_voyage_data_1],
    'Events': [_mock_event_data_1, _mock_event_data_2],
    'EventDetails': [_mock_event_detail_data_1, _mock_event_detail_data_2],
    'Geos': [_mock_geo_data_1, _mock_geo_data_2]
}

_mock_voyages_paged_flat_response_data_1 = {
    'NextPageToken': 'ASDF',
    'Data': _mock_flat_voyages_data_1
}
_mock_voyages_paged_flat_response_data_2 = {
    'Data': {'Voyages': [_mock_flat_voyage_data_2],
             'Events': [],
             'EventDetails': [],
             'Geos': []}
}

_mock_voyages_paged_flat_response_2 = VoyagesFlatPagedResponse(
    data=VoyagesFlat((_mock_flat_voyage_2,), (), (), ())
)

_mock_flat_voyages_1 = VoyagesFlat(
    voyages=(_mock_flat_voyage_1,),
    events=(_mock_event_1, _mock_event_2),
    event_details=(_mock_event_detail_1, _mock_event_detail_2),
    geos=(_mock_geo_1, _mock_geo_2)
)

_mock_flat_voyages = VoyagesFlat(
    voyages=(_mock_flat_voyage_1, _mock_flat_voyage_2),
    events=(_mock_event_1, _mock_event_2),
    event_details=(_mock_event_detail_1, _mock_event_detail_2),
    geos=(_mock_geo_1, _mock_geo_2)
)

_mock_nested_event_data_1 = copy(_mock_event_data_1)
_mock_nested_event_data_1['EventDetails'] = [_mock_event_detail_data_1,
                                             _mock_event_detail_data_2]
_mock_nested_event_data_2 = copy(_mock_event_data_2)
_mock_nested_event_data_2['EventDetails'] = []
_mock_nested_voyage_data_1 = copy(_mock_flat_voyage_data_1)
_mock_nested_voyage_data_1['Events'] = [_mock_nested_event_data_1,
                                        _mock_nested_event_data_2]
_mock_nested_voyage_data_2 = copy(_mock_flat_voyage_data_2)
_mock_nested_voyage_data_2['Events'] = []

_mock_voyages_paged_nested_response_data_1 = {
    'NextPageToken': 'ASDF',
    'Data': [_mock_nested_voyage_data_1]
}
_mock_voyages_paged_nested_response_data_2 = \
    {'Data': [_mock_nested_voyage_data_2]}

_mock_nested_event_1 = dataclasses.replace(
    _mock_event_1,
    event_details=(_mock_event_detail_1, _mock_event_detail_2))
_mock_nested_event_2 = dataclasses.replace(
    _mock_event_2,
    event_details=())
_mock_nested_voyage_1 = dataclasses.replace(
    _mock_flat_voyage_1,
    events=(_mock_nested_event_1, _mock_nested_event_2))
_mock_nested_voyage_2 = dataclasses.replace(_mock_flat_voyage_2, events=())

_mock_voyages = (_mock_nested_voyage_1, _mock_nested_voyage_2)

_mock_get_advanced_search = {
    'input' : {
    'vessel_class_id' : 84,
    'first_load_arrival_date_from' : '2021-06-04',
    'first_load_arrival_date_to' : '2021-07-04',
    'hide_event_details' : True,
    'hide_events' : True,
    'hide_market_info' : False
    },

    'expected_output' : 
                 'voyages-api/v2/search/advanced/?'\
                 'VesselClassId=84&'\
                 'FirstLoadArrivalDateFrom=2021-06-04&'\
        	     'FirstLoadArrivalDateTo=2021-07-04&'\
                 'HideEventDetails=True&'\
                 'HideEvents=True&'\
                 'HideMarketInfo=False'
}

_mock_advanced_search_response_data = {
    'ID' : '91017.130',
    'IMO' : '91017',
    'VoyageNumber' : 65,
    'Horizon' : 'Current',
    'VesselName' : 'Signal Vessel',
    'VesselTypeID' : 1,
    'VesselType' : 'Tanker',
    'VesselClassID' : 84,
    'VesselClass' : 'VLCC',
    'TradeID' : 1,
    'Trade' : 'Crude',
    'VesselStatusID' : 1,
    'VesselStatus': 'Voyage',
    'CommercialOperatorID': 1797,
    'CommercialOperator': 'Signal',
    'StartDate': '2020-12-23T14:42:00Z',
    'FirstLoadArrivalDate': '2021-06-11T12:09:11.131Z',
    'EndDate': '2021-07-20T23:44:51.004Z',
    'ChartererID': -1,
    'Charterer': 'Unknown',
    'CargoTypeID': -2,
    'CargoType': 'Not set',
    'CargoGroupID': -32,
    'CargoGroup': 'Not set',
    'CargoTypeSource': 'Estimated',
    'LaycanFrom': '2021-06-11T12:09:11.131Z',
    'LaycanTo': '2021-06-14T01:22:40.829Z',
    'FixtureStatusID': 5,
    'FixtureStatus': 'PossFixed',
    'FixtureDate': '2021-05-26T07:53:40Z',
    'FixtureIsCOA': False,
    'FixtureIsHold': False,
    'IsImpliedByAIS': True,
    'BallastDistance': 9036.45
}

_mock_advanced_search_voyage = Voyage(
    imo = 91017, voyage_number = 65, 
    vessel_type_id = 1, vessel_class_id = 84, 
    vessel_status_id = 1, vessel_class = 'VLCC', trade_id = 1, 
    vessel_type = 'Tanker', trade = 'Crude', vessel_status = 'Voyage',
    commercial_operator_id = 1797, id= '91017.130', vessel_name = 'Signal Vessel',
    commercial_operator = 'Signal', 
    start_date = datetime.fromisoformat(
        '2020-12-23T14:42:00'
    ).replace(tzinfo=timezone.utc), first_load_arrival_date = datetime.fromisoformat(
        '2021-06-11T12:09:11.131'
    ).replace(tzinfo=timezone.utc), end_date = datetime.fromisoformat(
        '2021-07-20T23:44:51.004'
    ).replace(tzinfo=timezone.utc),
    charterer_id = -1, charterer = 'Unknown',
    rate = None, rate_type = None,
    ballast_bonus = None, ballast_bonus_type = None, 
    cargo_type_id = -2, cargo_type = 'Not set',
    cargo_group_id = -32, cargo_group = 'Not set',
    cargo_type_source = 'Estimated',
    laycan_from = datetime.fromisoformat(
        '2021-06-11T12:09:11.131'
    ).replace(tzinfo=timezone.utc), laycan_to = datetime.fromisoformat(
        '2021-06-14T01:22:40.829'
    ).replace(tzinfo=timezone.utc),
    fixture_status_id = 5, fixture_status = 'PossFixed',
    fixture_date = datetime.fromisoformat(
        '2021-05-26T07:53:40'
    ).replace(tzinfo=timezone.utc), fixture_is_coa = False,
    fixture_is_hold = False, is_implied_by_ais = True,
    has_manual_entries = None,
    ballast_distance = 9036.45, laden_distance = None
)


@pytest.mark.parametrize("imo, vessel_class_id, vessel_type_id, date_from, "
                         "nested, incremental, expected",
                         [(None, None, None, None, True, True,
                           'voyages-api/v2/voyages/incremental'),
                          (None, None, None, None, False, True,
                           'voyages-api/v2/voyagesflat/incremental'),
                          (9436006, None, None, None, True, None,
                           'voyages-api/v2/voyages/imo/9436006'),
                          (9436006, None, None, None, False, None,
                           'voyages-api/v2/voyagesflat/imo/9436006'),
                          (9436006, None, None, None, True, True,
                           'voyages-api/v2/voyages/imo/9436006/incremental'),
                          (9436006, None, None, None, False, True,
                           'voyages-api/v2/voyagesflat/imo/9436006/'
                           'incremental'),
                          (9436006, 84, None, None, True, None,
                           'voyages-api/v2/voyages/imo/9436006'),
                          (None, 84, None, None, True, None,
                           'voyages-api/v2/voyages/class/84'),
                          (None, 84, None, None, False, None,
                           'voyages-api/v2/voyagesflat/class/84'),
                          (None, 84, None, None, True, True,
                           'voyages-api/v2/voyages/class/84/incremental'),
                          (None, 84, None, None, False, True,
                           'voyages-api/v2/voyagesflat/class/84/incremental'),
                          (None, 84, None, date(2020, 1, 1), True, None,
                           'voyages-api/v2/voyages/class/84/date/2020-01-01'),
                          (None, 84, None, date(2020, 1, 1), False, None,
                           'voyages-api/v2/voyagesflat/class/84/date/'
                           '2020-01-01'),
                          (None, 84, None, date(2020, 1, 1), True, True,
                           'voyages-api/v2/voyages/class/84/date/2020-01-01/'
                           'incremental'),
                          (None, 84, None, date(2020, 1, 1), False, True,
                           'voyages-api/v2/voyagesflat/class/84/date/'
                           '2020-01-01/incremental'),
                          (None, None, 1, None, True, True,
                           'voyages-api/v2/voyages/type/1/incremental')])
def test_get_endpoint(imo, vessel_class_id, vessel_type_id, date_from, nested,
                      incremental, expected):
    endpoint = VoyagesAPI._get_endpoint(
        imo=imo,
        vessel_class_id=vessel_class_id,
        vessel_type_id=vessel_type_id,
        date_from=date_from,
        nested=nested,
        incremental=incremental)
    assert endpoint == expected


def test_get_endpoint_error_no_arguments():
    with pytest.raises(NotImplementedError):
        VoyagesAPI._get_endpoint()


def test_get_endpoint_error_vessel_type_no_date_non_incremental():
    with pytest.raises(NotImplementedError):
        VoyagesAPI._get_endpoint(vessel_type_id=1, date_from=None,
                                 incremental=False)


def test_get_advanced_endpoint():
    expected = _mock_get_advanced_search['expected_output']
    endpoint = VoyagesAPI._get_advanced_endpoint(**_mock_get_advanced_search['input'])
    assert endpoint == expected


def create_voyages_api(response_data: Union[Dict, List] = None) \
        -> Tuple[VoyagesAPI, MagicMock]:
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = response_data
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesAPI(connection)
    return api, mocked_make_request


def create_voyages_api_multiple_requests(
        responses_data: List[Union[Dict, List]]) \
        -> Tuple[VoyagesAPI, MagicMock]:
    connection = Connection('', '')
    response = MagicMock()
    response.json = MagicMock(side_effect=responses_data)
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesAPI(connection)
    return api, mocked_make_request


def test_voyages_api_pages_flat():
    mock_responses = [_mock_voyages_paged_flat_response_data_1,
                      _mock_voyages_paged_flat_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_responses)
    voyages, _ = api._get_voyages_flat_pages('')
    assert voyages == _mock_flat_voyages


def test_voyages_api_pages_nested():
    mock_responses = [_mock_voyages_paged_nested_response_data_1,
                      _mock_voyages_paged_nested_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_responses)
    voyages, _ = api._get_voyages_pages('')
    assert voyages == _mock_voyages


def test_get_voyages_imo_requests():
    mock_response = [_mock_nested_voyage_data_1, _mock_nested_voyage_data_2]
    imo = _mock_nested_voyage_1.imo
    api, mocked_make_request = create_voyages_api(mock_response)
    _ = api.get_voyages(imo)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url, f'voyages/imo/{imo}'),
        query_string=None)


def test_get_voyages_imo_returns():
    mock_response = [_mock_nested_voyage_data_1, _mock_nested_voyage_data_2]
    imo = _mock_nested_voyage_1.imo
    api, _ = create_voyages_api(mock_response)
    voyages = api.get_voyages(imo)
    assert voyages == (_mock_nested_voyage_1, _mock_nested_voyage_2)


def test_get_voyages_flat_imo_requests():
    mock_response = _mock_flat_voyages_data_1
    imo = _mock_flat_voyage_1.imo
    api, mocked_make_request = create_voyages_api(mock_response)
    _ = api.get_voyages_flat(imo)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url, f'voyagesflat/imo/{imo}'),
        query_string=None)


def test_get_voyages_flat_imo_returns():
    mock_response = _mock_flat_voyages_data_1
    imo = _mock_flat_voyage_1.imo
    api, _ = create_voyages_api(mock_response)
    voyages = api.get_voyages_flat(imo)
    assert voyages == _mock_flat_voyages_1
 

def test_get_voyages_class_requests():
    mock_responses = [_mock_voyages_paged_nested_response_data_1,
                      _mock_voyages_paged_nested_response_data_2]
    next_page_token = \
        _mock_voyages_paged_nested_response_data_1['NextPageToken']
    vessel_class_id = 84
    api, mocked_make_request = create_voyages_api_multiple_requests(
        mock_responses)
    _ = api.get_voyages(vessel_class_id=vessel_class_id)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url, f'voyages/class/{vessel_class_id}'),
        query_string={'token': next_page_token})


def test_get_voyages_class_returns():
    mock_response = [_mock_voyages_paged_nested_response_data_1,
                     _mock_voyages_paged_nested_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_response)
    voyages = api.get_voyages(vessel_class_id=84)
    assert voyages == (_mock_nested_voyage_1, _mock_nested_voyage_2)


def test_get_voyages_flat_class_requests():
    mock_responses = [_mock_voyages_paged_flat_response_data_1,
                      _mock_voyages_paged_flat_response_data_2]
    next_page_token = \
        _mock_voyages_paged_nested_response_data_1['NextPageToken']
    vessel_class_id = 84
    api, mocked_make_request = create_voyages_api_multiple_requests(
        mock_responses)
    _ = api.get_voyages_flat(vessel_class_id=vessel_class_id)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url,
                f'voyagesflat/class/{vessel_class_id}'),
        query_string={'token': next_page_token})


def test_get_voyages_flat_class_returns():
    mock_response = [_mock_voyages_paged_flat_response_data_1,
                     _mock_voyages_paged_flat_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_response)
    voyages = api.get_voyages_flat(vessel_class_id=84)
    assert voyages == _mock_flat_voyages


def test_get_incremental_voyages_type_requests():
    mock_responses = [_mock_voyages_paged_nested_response_data_1,
                      _mock_voyages_paged_nested_response_data_2]
    next_page_token = \
        _mock_voyages_paged_nested_response_data_1['NextPageToken']
    vessel_type_id = 1
    api, mocked_make_request = create_voyages_api_multiple_requests(
        mock_responses)
    _ = api.get_incremental_voyages(vessel_type_id=vessel_type_id)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url,
                f'voyages/type/{vessel_type_id}/incremental'),
        query_string={'token': next_page_token})


def test_get_incremental_voyages_type_returns():
    mock_response = [_mock_voyages_paged_nested_response_data_1,
                     _mock_voyages_paged_nested_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_response)
    voyages, _ = api.get_incremental_voyages(vessel_type_id=1)
    assert voyages == (_mock_nested_voyage_1, _mock_nested_voyage_2)


def test_get_incremental_voyages_flat_type_requests():
    mock_responses = [_mock_voyages_paged_flat_response_data_1,
                      _mock_voyages_paged_flat_response_data_2]
    next_page_token = \
        _mock_voyages_paged_nested_response_data_1['NextPageToken']
    vessel_type_id = 1
    api, mocked_make_request = create_voyages_api_multiple_requests(
        mock_responses)
    _ = api.get_incremental_voyages_flat(vessel_type_id=vessel_type_id)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesAPI.relative_url,
                f'voyagesflat/type/{vessel_type_id}/incremental'),
        query_string={'token': next_page_token})


def test_get_incremental_voyages_flat_type_returns():
    mock_response = [_mock_voyages_paged_flat_response_data_1,
                     _mock_voyages_paged_flat_response_data_2]
    api, _ = create_voyages_api_multiple_requests(mock_response)
    voyages, _ = api.get_incremental_voyages_flat(vessel_class_id=84)
    assert voyages == _mock_flat_voyages


def test_get_advanced_search_voyages():
    mock_response = {'Data' : [_mock_advanced_search_response_data]}
    api, _ = create_voyages_api(mock_response)
    results = api.get_voyages_by_advanced_search('')
    assert results[0] == _mock_advanced_search_voyage