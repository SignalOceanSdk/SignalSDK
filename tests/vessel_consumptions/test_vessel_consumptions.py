from typing import Tuple
from unittest.mock import MagicMock

import requests

from signal_ocean import Connection
from vessel_consumptions_mock_data import (
    __mock_consumptions_response,
    __mock_consumptions,
    __mock_consumptions_minimal_response,
    __mock_consumptions_minimal,
    __mock_advertised_consumptions_response,
    __mock_advertised_consumptions,
    __mock_advertised_consumptions_minimal_response,
    __mock_advertised_consumptions_minimal,
    __mock_advertised_consumptions_page_response,
    __mock_advertised_consumptions_page,
    __mock_advertised_consumptions_page_empty_response,
    __mock_advertised_consumptions_page_empty,
)
from signal_ocean.vessel_consumptions.vessel_consumptions_api import (
    VesselConsumptionsAPI,
)


def create_vessel_consumptions_api(
    response: requests.Response,
) -> Tuple[VesselConsumptionsAPI, MagicMock]:
    connection = Connection()
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VesselConsumptionsAPI(connection)
    return api, mocked_make_request


# --- get_consumptions tests ---


def test_get_consumptions():
    response = MagicMock()
    response.json.return_value = __mock_consumptions_response
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_consumptions(imo=9412036)
    assert result == __mock_consumptions


def test_get_consumptions_minimal():
    response = MagicMock()
    response.json.return_value = __mock_consumptions_minimal_response
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_consumptions(imo=9412036)
    assert result == __mock_consumptions_minimal


def test_get_consumptions_not_found():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_consumptions(imo=0)
    assert result is None


# --- get_advertised_consumptions tests ---


def test_get_advertised_consumptions():
    response = MagicMock()
    response.json.return_value = __mock_advertised_consumptions_response
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions(imo=9412036)
    assert result == __mock_advertised_consumptions


def test_get_advertised_consumptions_minimal():
    response = MagicMock()
    response.json.return_value = (
        __mock_advertised_consumptions_minimal_response
    )
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions(imo=9876543)
    assert result == __mock_advertised_consumptions_minimal


def test_get_advertised_consumptions_not_found():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions(imo=0)
    assert result is None


def test_get_advertised_consumptions_no_content():
    response = MagicMock()
    response.status_code = requests.codes.no_content
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions(imo=9412036)
    assert result is None


# --- get_advertised_consumptions_paginated tests ---


def test_get_advertised_consumptions_paginated():
    response = MagicMock()
    response.json.return_value = (
        __mock_advertised_consumptions_page_response
    )
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions_paginated()
    assert result == __mock_advertised_consumptions_page


def test_get_advertised_consumptions_paginated_empty():
    response = MagicMock()
    response.json.return_value = (
        __mock_advertised_consumptions_page_empty_response
    )
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions_paginated()
    assert result == __mock_advertised_consumptions_page_empty


def test_get_advertised_consumptions_paginated_not_found():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, mocked_make_request = create_vessel_consumptions_api(response)
    result = api.get_advertised_consumptions_paginated(
        token="abc", page_size=10
    )
    assert result is None


# --- to_dict / repr tests ---


def test_vessel_consumptions_to_dict():
    result = __mock_consumptions.to_dict()
    assert result["Imo"] == 9412036
    assert result["IdleConsumption"] == 3.5
    assert "LadenConsumptions" in result
    assert len(result["LadenConsumptions"]) == 2
    assert result["LadenConsumptions"][0]["Speed"] == 12.5


def test_vessel_consumptions_repr():
    r = repr(__mock_consumptions_minimal)
    assert "VesselConsumptions" in r
    assert "imo=9412036" in r
    assert "idle_consumption=2.0" in r
    assert "laden_consumptions" not in r


def test_advertised_consumptions_to_dict():
    result = __mock_advertised_consumptions.to_dict()
    assert result["Imo"] == 9412036
    assert "BallastConsumptions" in result
    assert result["BallastConsumptions"][0]["MainFuelType"] == "VLSFO"


def test_advertised_consumptions_repr():
    r = repr(__mock_advertised_consumptions_minimal)
    assert "AdvertisedConsumptions" in r
    assert "imo=9876543" in r
    assert "ballast_consumptions" not in r


def test_advertised_consumptions_page_to_dict():
    result = __mock_advertised_consumptions_page.to_dict()
    assert result["NextPageToken"] == "abc123"
    assert len(result["Data"]) == 2
    assert result["Data"][0]["Imo"] == 9412036
