from unittest.mock import MagicMock
from typing import Tuple

import requests

from signal_ocean import Connection
from signal_ocean.geos import GeosAPI


def create_geo_api(response: requests.Response) -> Tuple[GeosAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = GeosAPI(connection)

    return (api, connection)


def test_returns_None_if_country_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    countries = api.get_countries(countryId=-999)
    
    assert len(countries) == 0


def test_requests_country_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    country = api.get_countries(countryId=123)

    connection._make_get_request.assert_called_with("geos-api/v2/countries/123", query_string=None)


def test_returns_requested_country():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    countries = api.get_countries(countryId=123)

    assert isinstance(countries, tuple)


def test_returns_None_if_port_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    ports = api.get_ports(portId=-999)

    assert len(ports) == 0


def test_requests_port_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    port = api.get_ports(portId=123)

    connection._make_get_request.assert_called_with("geos-api/v2/ports/123", query_string=None)


def test_returns_requested_port():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    ports = api.get_ports(portId=123)

    assert isinstance(ports, tuple)


def test_returns_None_if_area_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    areas = api.get_areas(areaId=-999)

    assert len(areas) == 0


def test_requests_area_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    area = api.get_areas(areaId=123)

    connection._make_get_request.assert_called_with("geos-api/v2/areas/123", query_string=None)


def test_returns_requested_area():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    areas = api.get_areas(areaId=123)

    assert isinstance(areas, tuple)

def test_returns_None_if_geo_asset_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, *_ = create_geo_api(response)

    geoAssets = api.get_geoAssets(geoAssetId=-999)
    
    assert len(geoAssets) == 0


def test_requests_geo_asset_by_id():
    response = MagicMock()
    response.json.return_value = {}
    api, connection = create_geo_api(response)

    geoAsset = api.get_geoAssets(geoAssetId=123)

    connection._make_get_request.assert_called_with("geos-api/v2/geoAssets/123", query_string=None)

def test_returns_requested_geo_asset():
    response = MagicMock()
    response.json.return_value = {}
    api, *_ = create_geo_api(response)

    geoAssets = api.get_geoAssets(geoAssetId=123)

    assert isinstance(geoAssets, tuple)