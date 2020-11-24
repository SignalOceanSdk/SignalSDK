from unittest.mock import MagicMock
from signal_ocean import Connection
from typing import Tuple
import requests
from signal_ocean.distances import DistancesAPI, RouteResponse, AlternativePath, PointsOnRoute, Point


def create_distances_api(response: requests.Response) -> Tuple[DistancesAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = DistancesAPI(connection)

    return (api, connection)

def test_requests_point_to_point_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_point_to_point_distance(vessel_class_id=86,
        loading_condition_id=1,
        latitude_from=42.5,
        latitude_to=32.5,
        longitude_from=55.6,
        longitude_to=78.8)

    excected_endpoint = "/api/v1/Distance/PointToPoint"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&latitudefrom={42.5}"
    excected_endpoint += f"&latitudeto={32.5}"
    excected_endpoint += f"&longitudefrom={55.6}"
    excected_endpoint += f"&longitudeto={78.8}"

    connection._make_get_request.assert_called_with(excected_endpoint)

def test_requests_point_to_point_route_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_point_to_point_route(vessel_class_id=86,
        loading_condition_id=1,
        latitude_from=42.5,
        latitude_to=32.5,
        longitude_from=55.6,
        longitude_to=78.8)

    excected_endpoint = "/api/v1/Distance/PointToPoint/Route"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&latitudefrom={42.5}"
    excected_endpoint += f"&latitudeto={32.5}"
    excected_endpoint += f"&longitudefrom={55.6}"
    excected_endpoint += f"&longitudeto={78.8}"

    connection._make_get_request.assert_called_with(excected_endpoint)

def test_requests_point_to_port_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_point_to_port_distance(vessel_class_id=86,
        loading_condition_id=1,
        latitude=42.5,
        longitude=32.5,
        port_id=3812)

    excected_endpoint = "/api/v1/Distance/PointToPort"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&latitude={42.5}"
    excected_endpoint += f"&longitude={32.5}"
    excected_endpoint += f"&portid={3812}"

    connection._make_get_request.assert_called_with(excected_endpoint)

def test_requests_point_to_port_route_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_point_to_port_route(vessel_class_id=86,
        loading_condition_id=1,
        latitude=42.5,
        longitude=32.5,
        port_id=3812)

    excected_endpoint = "/api/v1/Distance/PointToPort/Route"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&latitude={42.5}"
    excected_endpoint += f"&longitude={32.5}"
    excected_endpoint += f"&portid={3812}"

    connection._make_get_request.assert_called_with(excected_endpoint)

def test_requests_port_to_port_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_port_to_port_distance(vessel_class_id=86,
        loading_condition_id=1,
        port_id_from=3763,
        port_id_to=3812)

    excected_endpoint = "/api/v1/Distance/PortToPort"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&portIdFrom={3763}"
    excected_endpoint += f"&portIdTo={3812}"

    connection._make_get_request.assert_called_with(excected_endpoint)


def test_requests_port_to_port_route_with_params():
    response = MagicMock()

    api, connection = create_distances_api(response)

    api.get_port_to_port_route(vessel_class_id=86,
        loading_condition_id=1,
        port_id_from=3763,
        port_id_to=3812)

    excected_endpoint = "/api/v1/Distance/PortToPort/Route"
    excected_endpoint += f"?vesselclass={86}"
    excected_endpoint += f"&loadingcondition={1}"
    excected_endpoint += f"&portIdFrom={3763}"
    excected_endpoint += f"&portIdTo={3812}"

    connection._make_get_request.assert_called_with(excected_endpoint)