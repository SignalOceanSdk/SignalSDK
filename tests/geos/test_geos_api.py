from unittest.mock import MagicMock
from typing import Tuple

import requests

from signal_ocean import Connection
from signal_ocean.geos import GeosAPI, Country, Port, Area


def create_geo_api(response: requests.Response) -> Tuple[GeosAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = GeosAPI(connection)

    return (api, connection)


def test_returns_None_if_country_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    country = api.get_country(country_id=123)

    assert country is None


def test_requests_country_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    country = api.get_country(country_id=123)

    connection._make_get_request.assert_called_with("geo/countries/123")


def test_returns_requested_country():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    country = api.get_country(country_id=123)

    assert type(country) is Country


def test_returns_None_if_port_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    port = api.get_port(port_id=123)

    assert port is None


def test_requests_port_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    port = api.get_port(port_id=123)

    connection._make_get_request.assert_called_with("geo/ports/123")


def test_returns_requested_port():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    port = api.get_port(port_id=123)

    assert type(port) is Port


def test_returns_None_if_area_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    area = api.get_area(area_id=123)

    assert area is None


def test_requests_area_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    area = api.get_area(area_id=123)

    connection._make_get_request.assert_called_with("geo/areas/123")


def test_returns_requested_area():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    area = api.get_area(area_id=123)

    assert type(area) is Area
