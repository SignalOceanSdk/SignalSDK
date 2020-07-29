from decimal import Decimal
from unittest.mock import patch, MagicMock, ANY
from typing import Callable

import requests

from signal_ocean.vessel_valuations import VesselValuationsAPI, ValuationSummary


def test_requests_latest_valuation_for_specified_IMO():
    connection = MagicMock()
    connection._api_host = 'apihost/'
    api = VesselValuationsAPI(connection)
    response = MagicMock()
    response.text = None

    with patch('requests.get', return_value=response) as requests_get:
        api.get_latest_valuation(imo=123)

    requests_get.assert_called_with(
        'apihost/valuations/SnPValuation/lastvaluation/123',
        headers=ANY
    )


def test_gets_latest_valuation():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.text = '12.34'

    with patch('requests.get', return_value=response):
        valuation = api.get_latest_valuation(imo=123)

    assert valuation == Decimal('12.34')


def test_returns_None_if_there_is_no_latest_valuation():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.status_code = requests.codes.not_found

    with patch('requests.get', return_value=response):
        valuation = api.get_latest_valuation(imo=123)

    assert valuation is None


def test_requests_latest_valuation_summary_for_specified_IMO():
    connection = MagicMock()
    connection._api_host = 'apihost/'
    api = VesselValuationsAPI(connection)
    response = MagicMock()
    response.json.return_value = {}

    with patch('requests.get', return_value=response) as requests_get:
        api.get_latest_valuation_summary(imo=123)

    requests_get.assert_called_with(
        'apihost/valuations/SnPValuation/lastvaluation/shortdetails/123',
        headers=ANY
    )


def test_gets_latest_valuation_summary():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.json.return_value = {}

    with patch('requests.get', return_value=response):
        valuation = api.get_latest_valuation_summary(imo=123)

    assert type(valuation) is ValuationSummary


def test_returns_None_if_there_is_no_latest_valuation_summary():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.status_code = requests.codes.not_found

    with patch('requests.get', return_value=response):
        valuation = api.get_latest_valuation_summary(imo=123)

    assert valuation is None


def test_requests_valuation_history_for_specified_IMO():
    connection = MagicMock()
    connection._api_host = 'apihost/'
    api = VesselValuationsAPI(connection)
    response = MagicMock()
    response.json.return_value = []

    with patch('requests.get', return_value=response) as requests_get:
        api.get_valuation_history(imo=123)

    requests_get.assert_called_with(
        'apihost/valuations/SnPValuation/allvaluations/shortdetails/123',
        headers=ANY
    )


def test_gets_valuation_history():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.json.return_value = [{}, {}]

    with patch('requests.get', return_value=response):
        valuations = api.get_valuation_history(imo=123)

    assert len(valuations) == 2
    assert type(valuations[0]) is ValuationSummary
    assert type(valuations[1]) is ValuationSummary


def test_returns_None_if_there_are_no_valuation_summaries():
    api = VesselValuationsAPI()
    response = MagicMock()
    response.status_code = requests.codes.not_found

    with patch('requests.get', return_value=response):
        valuations = api.get_valuation_history(imo=123)

    assert valuations is None
