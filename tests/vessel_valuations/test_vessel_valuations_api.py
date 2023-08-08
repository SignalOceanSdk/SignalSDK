from unittest.mock import MagicMock
from typing import Tuple

import requests

from signal_ocean.vessel_valuations import VesselValuationsAPI, Valuation
from tests.vessel_valuations.mock_data import __mock_valuation_imo, __mock_valuation_imo_response, \
    __mock_historical_valuations_no_args, __mock_response_historical_valuations_no_args, __mock_valuation_page, \
    __mock_response_valuation_page, __mock_valuations_list, __mock_response_valuations_list
from signal_ocean import Connection


def create_valuations_api(response: requests.Response) -> Tuple[VesselValuationsAPI, MagicMock]:
    connection = Connection()
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VesselValuationsAPI(connection)
    return api, mocked_make_request


def test_get_historical_valuations_for_imo():
    response = MagicMock()
    response.json.return_value = __mock_historical_valuations_no_args
    api, mocked_make_request = create_valuations_api(response)
    valuation = api.get_all_historical_valuations_by_imo(imo=9414254)
    assert valuation == __mock_response_historical_valuations_no_args


def test_gets_latest_valuation_price():
    response = MagicMock()
    response.json.return_value = __mock_valuation_imo
    api, mocked_make_request = create_valuations_api(response)

    valuation = api.get_latest_valuation_by_imo(imo=9414254)

    assert valuation == __mock_valuation_imo_response


def test_returns_none_if_there_is_no_latest_valuation_price():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, mocked_make_request = create_valuations_api(response)

    valuation = api.get_latest_valuation_by_imo(imo=123)

    assert valuation is None


def test_get_latest_valuations_by_page():
    response = MagicMock()
    response.json.return_value = __mock_valuation_page
    api, mocked_make_request = create_valuations_api(response)
    page = api.get_latest_valuations_by_page(page=1)
    assert page == __mock_response_valuation_page


# def test_get_latest_valuations_for_list_of_vessels():
#     response = MagicMock()
#     response.json.return_value = __mock_valuations_list
#     api, mocked_make_request = create_valuations_api(response)
#     valuations_list = api.get_latest_valuations_for_list_of_vessels(
#         imo_list=[9180803])
#     assert valuations_list == __mock_response_valuations_list

