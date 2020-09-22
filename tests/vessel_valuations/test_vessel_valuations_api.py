from decimal import Decimal
from unittest.mock import patch, MagicMock, ANY
from typing import Tuple

import requests

from signal_ocean.vessel_valuations import VesselValuationsAPI, Valuation
from signal_ocean import Connection


def create_valuations_api(
        response: requests.Response) -> Tuple[VesselValuationsAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = VesselValuationsAPI(connection)

    return (api, connection)

def test_requests_latest_valuation_price_for_specified_IMO():
    response = MagicMock()
    response.text = None
    api, connection = create_valuations_api(response)

    api.get_latest_valuation_price(imo=123)

    connection._make_get_request.assert_called_with(
        'valuations/SnPValuation/lastvaluation/123'
    )


def test_gets_latest_valuation_price():
    response = MagicMock()
    response.text = '12.34'
    api, *_ = create_valuations_api(response)

    valuation = api.get_latest_valuation_price(imo=123)

    assert valuation == Decimal('12.34')


def test_returns_None_if_there_is_no_latest_valuation_price():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_valuations_api(response)

    valuation = api.get_latest_valuation_price(imo=123)

    assert valuation is None


def test_requests_latest_valuation_for_specified_IMO():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_valuations_api(response)

    api.get_latest_valuation(imo=123)

    connection._make_get_request.assert_called_with(
        'valuations/SnPValuation/lastvaluation/shortdetails/123'
    )


def test_gets_latest_valuation():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_valuations_api(response)

    valuation = api.get_latest_valuation(imo=123)

    assert type(valuation) is Valuation


def test_returns_None_if_there_is_no_latest_valuation():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_valuations_api(response)

    valuation = api.get_latest_valuation(imo=123)

    assert valuation is None


def test_requests_all_valuations_for_specified_IMO():
    response = MagicMock()
    response.json.return_value = []
    api, connection = create_valuations_api(response)

    api.get_valuations(imo=123)

    connection._make_get_request.assert_called_with(
        'valuations/SnPValuation/allvaluations/shortdetails/123'
    )


def test_gets_all_valuations():
    response = MagicMock()
    response.json.return_value = [{}, {}]
    api, *_ = create_valuations_api(response)

    valuations = api.get_valuations(imo=123)

    assert len(valuations) == 2
    assert type(valuations[0]) is Valuation
    assert type(valuations[1]) is Valuation


def test_returns_None_if_there_are_no_valuations():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_valuations_api(response)

    valuations = api.get_valuations(imo=123)

    assert valuations is None
