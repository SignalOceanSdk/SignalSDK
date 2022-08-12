from datetime import datetime, timezone
from typing import Tuple
from unittest.mock import MagicMock
from urllib.parse import urljoin

import requests

from signal_ocean import Connection
from signal_ocean.vessels.models import Vessel, VesselClass, VesselType
from signal_ocean.vessels.vessels_api import VesselsAPI

__mock_vessel_classes_response = (
    {'Id': 86, 'Name': 'Aframax', 'VesselTypeID': 1, 'VesselType': 'Tanker',
     'FromSize': 82000, 'ToSize': 124999,
     'DefiningSize': 'DeadWeight', 'Size': 'kt'},
    {'Id': 74, 'Name': 'Panamax Dry', 'VesselTypeID': 3, 'VesselType': 'Dry',
     'FromSize': 67000, 'ToSize': 84999,
     'DefiningSize': 'DeadWeight', 'Size': 'kt'})

__mock_vessel_classes = (
    VesselClass(id=86, name='Aframax', vessel_type_id=1, vessel_type='Tanker',
                from_size=82000, to_size=124999,
                defining_size='DeadWeight', size='kt'),
    VesselClass(id=74, name='Panamax Dry', vessel_type_id=3, vessel_type='Dry',
                from_size=67000, to_size=84999,
                defining_size='DeadWeight', size='kt'))

__mock_vessel_types_response = [{'Id': 3, 'Name': 'Dry'},
                                {'Id': 1, 'Name': 'Tanker'}]

__mock_vessel_types = (VesselType(id=3, name='Dry'),
                       VesselType(id=1, name='Tanker'))

__mock_vessel_response_1 = {'IMO': 1, 'VesselName': 'Signal 1',
                            'CallSign': 'AAA', 'VesselTypeID': 1,
                            'VesselType': 'Tanker', 'BuiltForTradeID': 1,
                            'BuiltForTrade': 'Crude', 'TradeID': 1,
                            'Trade': 'Crude', 'VesselClassID': 86,
                            'VesselClass': 'Aframax', 'FlagCode': 'MT',
                            'Flag': 'Malta', 'CommercialOperatorID': 1926,
                            'CommercialOperator': 'Signal Maritime',
                            'Deadweight': 112984, 'BreadthExtreme': 44,
                            'GrossRatedTonnage': 62775,
                            'ReducedGrossTonnage': 50063,
                            'NetRatedTonnage': 34934, 'Draught': 14.81,
                            'LengthOverall': 249.96, 'MouldedDepth': 21.0,
                            'YearBuilt': 2009, 'BuiltCountryCode': 'CN',
                            'BuiltCountryName': 'China',
                            'ShipyardBuiltID': 7188,
                            'ShipyardBuiltName': 'New Shipyard',
                            'CranesTonCapacity': 15, 'Geared': False,
                            'PanamaCanalNetTonnage': 51572,
                            'CubicSize': 124612,
                            'SummerTPC': 99.7,
                            'CleanDirtyWilling': False,
                            'LightshipTonnes': 20994,
                            'MainEngineManufacturer': 'MAN B&W',
                            'MainEngineManufacturerID': 1,
                            'DeliveryDate': '2009-05-26T00:00:00',
                            'ClassificationRegisterID': 2,
                            'ClassificationRegister': 'Bureau of Shipping',
                            'UpdatedDate': '2020-08-18T20:35:07.377'}

__mock_vessel_1 = Vessel(imo=1, vessel_name='Signal 1', call_sign='AAA',
                         vessel_type_id=1,
                         vessel_type='Tanker', built_for_trade_id=1,
                         built_for_trade='Crude', trade_id=1, trade='Crude',
                         vessel_class_id=86, vessel_class='Aframax',
                         flag_code='MT', flag='Malta',
                         commercial_operator_id=1926,
                         commercial_operator='Signal Maritime',
                         deadweight=112984,
                         breadth_extreme=44, gross_rated_tonnage=62775,
                         reduced_gross_tonnage=50063,
                         net_rated_tonnage=34934, draught=14.81,
                         length_overall=249.96, moulded_depth=21.0,
                         year_built=2009, built_country_code='CN',
                         built_country_name='China', shipyard_built_id=7188,
                         shipyard_built_name='New Shipyard',
                         cranes_ton_capacity=15, geared=False,
                         panama_canal_net_tonnage=51572, cubic_size=124612,
                         summer_tpc=99.7, clean_dirty_willing=False,
                         lightship_tonnes=20994,
                         main_engine_manufacturer='MAN B&W',
                         main_engine_manufacturer_id=1,
                         delivery_date=datetime.fromisoformat(
                             '2009-05-26T00:00:00').replace(
                             tzinfo=timezone.utc),
                         classification_register_id=2,
                         classification_register='Bureau of Shipping',
                         updated_date=datetime.fromisoformat(
                             '2020-08-18T20:35:07.377').replace(
                             tzinfo=timezone.utc))

__mock_vessel_response_2 = {'IMO': 2, 'VesselName': 'Signal 2',
                            'CallSign': 'BBB', 'VesselTypeID': 1,
                            'VesselType': 'Tanker', 'BuiltForTradeID': 1,
                            'BuiltForTrade': 'Crude', 'TradeID': 1,
                            'Trade': 'Crude', 'VesselClassID': 84,
                            'VesselClass': 'VLCC', 'FlagCode': 'BS',
                            'Flag': 'Bahamas', 'CommercialOperatorID': 1713,
                            'CommercialOperator': 'Signal',
                            'Deadweight': 318669, 'BreadthExtreme': 60,
                            'GrossRatedTonnage': 161382,
                            'ReducedGrossTonnage': 128481,
                            'NetRatedTonnage': 110526, 'Draught': 22.53,
                            'LengthOverall': 333.0, 'MouldedDepth': 30.4,
                            'YearBuilt': 2005, 'BuiltCountryCode': 'KR',
                            'BuiltCountryName': 'Korea, Republic of',
                            'ShipyardBuiltID': 6413,
                            'ShipyardBuiltName': 'Shipyard',
                            'CranesTonCapacity': 20, 'Geared': False,
                            'CubicSize': 339180,
                            'ScrubbersDate': '2020-04-19T11:57:00',
                            'SummerTPC': 180.79,
                            'CleanDirtyWilling': False,
                            'LightshipTonnes': 44262,
                            'MainEngineManufacturer': 'BW',
                            'MainEngineManufacturerID': 1,
                            'DeliveryDate': '2005-02-18T00:00:00',
                            'ClassificationRegisterID': 73,
                            'ClassificationRegister': "Register",
                            'UpdatedDate': '2020-08-18T13:10:21.930'}

__mock_vessel_2 = Vessel(imo=2, vessel_name='Signal 2', call_sign='BBB',
                         vessel_type_id=1, vessel_type='Tanker',
                         built_for_trade_id=1, built_for_trade='Crude',
                         trade_id=1, trade='Crude', vessel_class_id=84,
                         vessel_class='VLCC', flag_code='BS', flag='Bahamas',
                         commercial_operator_id=1713,
                         commercial_operator='Signal', deadweight=318669,
                         breadth_extreme=60,
                         gross_rated_tonnage=161382,
                         reduced_gross_tonnage=128481,
                         net_rated_tonnage=110526,
                         draught=22.53, length_overall=333.0,
                         moulded_depth=30.4, year_built=2005,
                         built_country_code='KR',
                         built_country_name='Korea, Republic of',
                         shipyard_built_id=6413,
                         shipyard_built_name='Shipyard',
                         cranes_ton_capacity=20,
                         geared=False,
                         cubic_size=339180,
                         scrubbers_date=datetime.fromisoformat(
                             '2020-04-19T11:57:00').replace(
                             tzinfo=timezone.utc),
                         summer_tpc=180.79, clean_dirty_willing=False,
                         lightship_tonnes=44262,
                         main_engine_manufacturer='BW',
                         main_engine_manufacturer_id=1,
                         delivery_date=datetime.fromisoformat(
                             '2005-02-18T00:00:00').replace(
                             tzinfo=timezone.utc),
                         classification_register_id=73,
                         classification_register="Register",
                         updated_date=datetime.fromisoformat(
                             '2020-08-18T13:10:21.930').replace(
                             tzinfo=timezone.utc))

__mock_vessels_response = (__mock_vessel_response_1, __mock_vessel_response_2)


def create_vessels_api(response: requests.Response) \
        -> Tuple[VesselsAPI, MagicMock]:
    connection = Connection('', '')
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VesselsAPI(connection)
    return api, mocked_make_request


def test_returns_none_if_vessel_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, _ = create_vessels_api(response)
    vessel = api.get_vessel(imo=5)
    assert vessel is None


def test_requests_vessel_by_id():
    response = MagicMock()
    response.json.return_value = __mock_vessel_response_1
    api, mocked_make_request = create_vessels_api(response)
    _ = api.get_vessel(imo=__mock_vessel_1.imo)
    mocked_make_request.assert_called_with(
        urljoin(VesselsAPI.relative_url, f'vessels/{__mock_vessel_1.imo}'),
        query_string=None)


def test_returns_vessel_by_id():
    response = MagicMock()
    response.json.return_value = __mock_vessel_response_1
    api, _ = create_vessels_api(response)
    vessel = api.get_vessel(imo=__mock_vessel_1.imo)
    assert vessel == __mock_vessel_1


def test_requests_vessel_classes():
    response = MagicMock()
    response.json.return_value = __mock_vessel_classes_response
    api, mocked_make_request = create_vessels_api(response)
    _ = api.get_vessel_classes()
    mocked_make_request.assert_called_with(
        urljoin(VesselsAPI.relative_url, 'vesselClasses'),
        query_string=None)


def test_response_vessel_classes():
    response = MagicMock()
    response.json.return_value = __mock_vessel_classes_response
    api, _ = create_vessels_api(response)
    vessel_classes = api.get_vessel_classes()
    assert vessel_classes == __mock_vessel_classes


def test_requests_vessel_types():
    response = MagicMock()
    response.json.return_value = __mock_vessel_types_response
    api, mocked_make_request = create_vessels_api(response)
    _ = api.get_vessel_types()
    mocked_make_request.assert_called_with(
        urljoin(VesselsAPI.relative_url, 'vesselTypes'),
        query_string=None)


def test_response_vessel_types():
    response = MagicMock()
    response.json.return_value = __mock_vessel_types_response
    api, _ = create_vessels_api(response)
    vessel_types = api.get_vessel_types()
    assert vessel_types == __mock_vessel_types


def test_requests_vessels():
    response = MagicMock()
    response.json.return_value = __mock_vessels_response
    api, mocked_make_request = create_vessels_api(response)
    _ = api.get_vessels()
    mocked_make_request.assert_called_with(
        urljoin(VesselsAPI.relative_url, 'vessels/all'),
        query_string=None)


def test_response_vessels():
    response = MagicMock()
    response.json.return_value = __mock_vessels_response
    api, _ = create_vessels_api(response)
    vessels = api.get_vessels()
    assert vessels == (__mock_vessel_1, __mock_vessel_2)


def test_requests_search_vessels():
    response = MagicMock()
    response.json.return_value = __mock_vessels_response
    api, mocked_make_request = create_vessels_api(response)
    _ = api.get_vessels('signal')
    mocked_make_request.assert_called_with(
        urljoin(VesselsAPI.relative_url, 'vessels/searchByName/signal'),
        query_string=None)
