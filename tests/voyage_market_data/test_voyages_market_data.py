import dataclasses
from datetime import datetime, date, timezone
import re
from typing import Tuple, Dict, Union, List
from unittest.mock import MagicMock
from urllib.parse import urljoin

import pytest

from signal_ocean import Connection
from signal_ocean.voyages_market_data.models import MatchedFixture, \
    Fixture, VoyagesMarketData, VoyagesMarketDataPagedResponse
from signal_ocean.voyages_market_data import VoyagesMarketDataAPI

_mock_voyages_market_data_1 = {
      "id": "MI96EC95VED7CF7700",
      "VoyageID": "I96EC95VED7CF7700",
      "IMO": 9890965,
      "VoyageNumber": 1,
      "VesselTypeID": 1,
      "VesselClassID": 84,
      "TradeID": 1,
      "CommercialOperatorID": 1713
    }

_mock_voyages_market_data_paged_response_1 = {
    'Data': {'Voyages': [_mock_voyages_market_data_1],
             'Events': [],
             'EventDetails': [],
             'Geos': []}
}

_mock_voyages_market_data_response_1 = {
  "Data": [
    {
      "ID": "MI96EC95VED7CF7700",
      "VoyageID": "I96EC95VED7CF7700",
      "IMO": 9890965,
      "VoyageNumber": 1,
      "VesselTypeID": 1,
      "VesselClassID": 84,
      "TradeID": 1,
      "CommercialOperatorID": 1713
    }
  ]
}

_mock_voyage_market_data_object = VoyagesMarketData(
    id = 'MI96EC95VED7CF7700', voyage_id= 'I96EC95VED7CF7700', imo=9890965,
    voyage_number=1, vessel_type_id=1, vessel_class_id = 84, trade_id = 1,
    commercial_operator_id = 1713
)

@pytest.mark.parametrize("imo, voyage_id, voyage_number, vessel_class_id, vessel_type_id, "
                           "incremental, include_vessel_details, include_fixtures, include_lineups, "
                          "include_positions, include_matched_fixture, include_labels, "
                          "expected",
                         [(9412036, None, None, None, None, None, 
                           None, None, None, None, None, None,
                 'voyages-market-data-api/v1/marketData/imo/9412036'),
                         (None, None, None, 84, None, None, 
                           None, None, None, None, None, None,
                 'voyages-market-data-api/v1/marketData/class/84'),
                         (9412036, None, None, None, None, None,
                          None, None, None, None, True, None,
                           'voyages-market-data-api/v1/marketData/imo/9412036?IncludeMatchedFixture=True')])

def test_get_endpoint(imo, voyage_id, voyage_number, vessel_class_id, vessel_type_id,
                       incremental, include_vessel_details, include_fixtures, include_lineups,
                       include_positions, include_matched_fixture, include_labels,
                       expected):
    endpoint = VoyagesMarketDataAPI._get_endpoint(
        imo=imo,
        voyage_id=voyage_id,
        voyage_number=voyage_number,
        vessel_class_id=vessel_class_id,
        vessel_type_id=vessel_type_id,
        incremental=incremental,
        include_vessel_details=include_vessel_details,
        include_fixtures=include_fixtures,
        include_lineups=include_lineups,
        include_positions=include_positions,
        include_matched_fixture=include_matched_fixture,
        include_labels=include_labels)
    assert endpoint == expected

def test_get_endpoint_error_no_arguments():
    with pytest.raises(NotImplementedError):
        VoyagesMarketDataAPI._get_endpoint()

def create_voyages_market_data_api(
        response_data: List[Union[Dict, List]]) \
        -> Tuple[VoyagesMarketDataAPI, MagicMock]:
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = response_data
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesMarketDataAPI(connection)
    return api, mocked_make_request

def test_voyages_market_data_imo_requests():
    mock_response = _mock_voyages_market_data_response_1
    imo = _mock_voyage_market_data_object.imo
    api, mocked_make_request = create_voyages_market_data_api(mock_response)
    _ = api.get_voyage_market_data(imo)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesMarketDataAPI.relative_url, f'marketData/imo/{imo}'),
        query_string=None)

def test_voyages_market_data_imo_voyage_number_requests():
    mock_response = _mock_voyages_market_data_response_1
    imo = _mock_voyage_market_data_object.imo
    voyage_number = _mock_voyage_market_data_object.voyage_number
    api, mocked_make_request = create_voyages_market_data_api(mock_response)
    _ = api.get_voyage_market_data(imo=imo, voyage_number=voyage_number)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesMarketDataAPI.relative_url, f'marketData/imo/{imo}/voyage/{voyage_number}'),
        query_string=None)

def test_voyages_market_data_vessel_class_requests():
    mock_response = _mock_voyages_market_data_response_1
    vessel_class_id = 84
    api, mocked_make_request = create_voyages_market_data_api(mock_response)
    _ = api.get_voyage_market_data(vessel_class_id=vessel_class_id)
    mocked_make_request.assert_called_with(
        urljoin(VoyagesMarketDataAPI.relative_url, f'marketData/class/{vessel_class_id}'),
        query_string=None)

def test_get_voyages_market_data_request_imo_voyage_number_return():
    mock_response = _mock_voyages_market_data_response_1
    imo = _mock_voyage_market_data_object.imo
    voyage_number = _mock_voyage_market_data_object.voyage_number
    api, _ = create_voyages_market_data_api(mock_response)
    voyage_market_data = api.get_voyage_market_data(imo=imo, voyage_number=voyage_number)
    assert voyage_market_data[0] == _mock_voyage_market_data_object
