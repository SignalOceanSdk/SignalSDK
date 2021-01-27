from unittest.mock import MagicMock
from typing import Tuple
from decimal import Decimal
from datetime import date

import requests

from signal_ocean import Connection
from signal_ocean.distances import (
    DistancesAPI,
    Point,
    Port,
    VesselClass,
    LoadingCondition,
    RouteRestrictions,
)


def create_port(port_id=1, name="port name") -> Port:
    return Port(port_id, name)


def create_vessel_class(vessel_id=1, name="vessel class name") -> VesselClass:
    return VesselClass(vessel_id, name)


def create_distances_api(
    response: requests.Response,
) -> Tuple[DistancesAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = DistancesAPI(connection)

    return (api, connection)


def test_requests_point_to_point_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)

    api.get_point_to_point_distance(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        start_point=Point(Decimal("42.5"), Decimal("55.6")),
        end_point=Point(Decimal("32.5"), Decimal("78.8")),
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PointToPoint",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "latitudefrom": "42.5",
            "latitudeto": "32.5",
            "longitudefrom": "55.6",
            "longitudeto": "78.8",
        },
    )


def test_requests_point_to_point_route_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)

    api.get_point_to_point_route(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        start_point=Point(Decimal("42.5"), Decimal("55.6")),
        end_point=Point(Decimal("32.5"), Decimal("78.8")),
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PointToPoint/Route",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "latitudefrom": "42.5",
            "latitudeto": "32.5",
            "longitudefrom": "55.6",
            "longitudeto": "78.8",
        },
    )


def test_requests_point_to_port_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)
    port_to = create_port(3812)

    api.get_point_to_port_distance(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        point=Point(Decimal("42.5"), Decimal("32.5")),
        port=port_to,
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PointToPort",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "latitude": "42.5",
            "longitude": "32.5",
            "portid": 3812,
        },
    )


def test_requests_point_to_port_route_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)
    port_to = create_port(3812)

    api.get_point_to_port_route(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        point=Point(Decimal("42.5"), Decimal("32.5")),
        port=port_to,
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PointToPort/Route",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "latitude": "42.5",
            "longitude": "32.5",
            "portid": 3812,
        },
    )


def test_requests_port_to_port_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)
    port_from = create_port(3763)
    port_to = create_port(3812)

    api.get_port_to_port_distance(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        port_from=port_from,
        port_to=port_to,
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PortToPort",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "portIdFrom": 3763,
            "portIdTo": 3812,
        },
    )


def test_requests_port_to_port_route_with_params():
    response = MagicMock()
    api, connection = create_distances_api(response)
    vessel_class = create_vessel_class(86)
    port_from = create_port(3763)
    port_to = create_port(3812)

    api.get_port_to_port_route(
        vessel_class=vessel_class,
        loading_condition_id=LoadingCondition.LADEN,
        port_from=port_from,
        port_to=port_to,
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/PortToPort/Route",
        {
            "vesselclass": 86,
            "loadingcondition": 1,
            "portIdFrom": 3763,
            "portIdTo": 3812,
        },
    )


def test_requests_generic_point_to_point_route_with_defaults():
    response = MagicMock()
    api, connection = create_distances_api(response)

    api.get_generic_point_to_point_route(
        Point(Decimal("1"), Decimal("2")), Point(Decimal("3"), Decimal("4"))
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/Generic",
        {
            "StartPointLatitude": "1",
            "StartPointLongitude": "2",
            "EndPointLatitude": "3",
            "EndPointLongitude": "4",
            "IsSuezOpen": None,
            "IsPanamaOpen": None,
            "IsPiracyConsidered": None,
            "IsMessinaOpen": None,
            "IsOresundOpen": None,
            "IsSuezOpenOnlyNorthbound": None,
            "DelaysValidAt": None,
            "GetAlternatives": None,
        },
    )


def test_requests_generic_point_to_point_route_with_restrictions():
    response = MagicMock()
    api, connection = create_distances_api(response)

    api.get_generic_point_to_point_route(
        Point(Decimal("1"), Decimal("2")),
        Point(Decimal("3"), Decimal("4")),
        RouteRestrictions(
            is_suez_open=True,
            is_panama_open=True,
            is_messina_open=True,
            is_oresund_open=True,
            is_suez_open_only_northbound=True,
            is_piracy_considered=True,
        ),
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/Generic",
        {
            "StartPointLatitude": "1",
            "StartPointLongitude": "2",
            "EndPointLatitude": "3",
            "EndPointLongitude": "4",
            "IsSuezOpen": True,
            "IsPanamaOpen": True,
            "IsPiracyConsidered": True,
            "IsMessinaOpen": True,
            "IsOresundOpen": True,
            "IsSuezOpenOnlyNorthbound": True,
            "DelaysValidAt": None,
            "GetAlternatives": None,
        },
    )


def test_requests_generic_point_to_point_route_with_delays_valid_at_date():
    response = MagicMock()
    api, connection = create_distances_api(response)

    api.get_generic_point_to_point_route(
        Point(Decimal("1"), Decimal("2")),
        Point(Decimal("3"), Decimal("4")),
        delays_valid_at=date(2020, 6, 15),
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/Generic",
        {
            "StartPointLatitude": "1",
            "StartPointLongitude": "2",
            "EndPointLatitude": "3",
            "EndPointLongitude": "4",
            "IsSuezOpen": None,
            "IsPanamaOpen": None,
            "IsPiracyConsidered": None,
            "IsMessinaOpen": None,
            "IsOresundOpen": None,
            "IsSuezOpenOnlyNorthbound": None,
            "DelaysValidAt": "2020-06-15",
            "GetAlternatives": None,
        },
    )


def test_requests_generic_point_to_point_route_with_alternatives():
    response = MagicMock()
    api, connection = create_distances_api(response)

    api.get_generic_point_to_point_route(
        Point(Decimal("1"), Decimal("2")),
        Point(Decimal("3"), Decimal("4")),
        get_alternatives=True,
    )

    connection._make_get_request.assert_called_with(
        "/distances-api/api/v1/Distance/Generic",
        {
            "StartPointLatitude": "1",
            "StartPointLongitude": "2",
            "EndPointLatitude": "3",
            "EndPointLongitude": "4",
            "IsSuezOpen": None,
            "IsPanamaOpen": None,
            "IsPiracyConsidered": None,
            "IsMessinaOpen": None,
            "IsOresundOpen": None,
            "IsSuezOpenOnlyNorthbound": None,
            "DelaysValidAt": None,
            "GetAlternatives": True,
        },
    )
