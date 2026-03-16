from decimal import Decimal
from signal_ocean.distances import _distances_json, RouteResponse, AlternativePath, PointsOnRoute, Point


def test_parse_route_response():
    route_response = {
        "id": 9999,
        "startPoint": {
            "lat": 42.500,
            "lon": 47.8,
        },
        "endPoint": {
            "lat": 52.500,
            "lon": 57.8,
        },
        "calculatedRoute": [
            {
                "lat": 42.500,
                "lon": 47.8,
            },
            {
                "lat": 52.500,
                "lon": 57.8,
            },
        ],
        "routingPointsOnRoute": [
            {
                "isHra": True,
                "isSeca": False,
                "distance": 4500.5,
                "distanceToEnter": 500.85,
                "heading": 200,
                "editable": False,
                "name": "Gibraltar",
                "isShown": True,
                "delayMins": False,
                "centerPoint": {
                    "lat": 42.500,
                    "lon": 47.8,
                    },
            },
            {
                "isHra": True,
                "isSeca": False,
                "distance": 5500.5,
                "distanceToEnter": 600.85,
                "heading": 100,
                "editable": True,
                "name": "Gela",
                "isShown": False,
                "delayMins": True,
                "centerPoint": {
                    "lat": 52.500,
                    "lon": 57.8,
                },
            },
        ],
        "distance": 8000.7,
        "piracyDistance": 9000.45,
        "secaDistance": 10000.89,
        "alternativePaths":[
            {
                "calculatedRoute": [
                    {
                        "lat": 42.500,
                        "lon": 47.8,
                    },
                    {
                        "lat": 52.500,
                        "lon": 57.8,
                    },
                ],
                "distance": 700.34,
                "routingPointsOnRoute": [
                    {
                        "isHra": True,
                        "isSeca": False,
                        "distance": 4500.5,
                        "distanceToEnter": 500.85,
                        "heading": 200,
                        "editable": False,
                        "name": "Gibraltar",
                        "isShown": True,
                        "delayMins": False,
                        "centerPoint": {
                            "lat": 42.500,
                            "lon": 47.8,
                            },
                    },
                    {
                        "isHra": True,
                        "isSeca": False,
                        "distance": 5500.5,
                        "distanceToEnter": 600.85,
                        "heading": 100,
                        "editable": True,
                        "name": "Gela",
                        "isShown": False,
                        "delayMins": True,
                        "centerPoint": {
                            "lat": 52.500,
                            "lon": 57.8,
                        },
                    },
        ],
        "piracyDistance": 1000.45,
        "secaDistance": 800.89,
            }
        ],
        "isEmpty": False,
        "bBox": [
            -69.11,
            33.55,
            23.69,
            37.62
        ]
    }

    result = _distances_json.parse_route_response(route_response)

    assert result.id == 9999
    assert result.start_point.lat == Decimal("42.500")
    assert result.start_point.lon == Decimal("47.8")
    assert result.end_point.lat == Decimal("52.500")
    assert result.end_point.lon == Decimal("57.8")

    assert len(result.calculated_route) == 2
    assert result.calculated_route[0] == Point(
        lat=Decimal("42.500"),
        lon=Decimal("47.8"))
    assert result.calculated_route[1] == Point(
        lat=Decimal("52.500"),
        lon=Decimal("57.8"))

    assert len(result.routing_points_on_route) == 2
    assert result.routing_points_on_route[0] == PointsOnRoute(
        is_hra=True,
        is_seca=False,
        distance=Decimal("4500.5"),
        distance_to_enter=Decimal("500.85"),
        heading=200,
        editable=False,
        name="Gibraltar",
        is_shown=True,
        delay_mins=False,
        center_point=Point(
            lat=Decimal("42.500"),
            lon=Decimal("47.8"),
        ),
    )
    assert result.routing_points_on_route[1] == PointsOnRoute(
        is_hra=True,
        is_seca=False,
        distance=Decimal("5500.5"),
        distance_to_enter=Decimal("600.85"),
        heading=100,
        editable=True,
        name="Gela",
        is_shown=False,
        delay_mins=True,
        center_point=Point(
            lat=Decimal("52.500"),
            lon=Decimal("57.8"),
        ),
    )

    assert result.distance == Decimal("8000.7")
    assert result.piracy_distance == Decimal("9000.45")
    assert result.seca_distance == Decimal("10000.89")

    assert result.is_empty == False
    assert len(result.bbox) == 4
    assert result.bbox[0] == Decimal("-69.11")
    assert result.bbox[1] == Decimal("33.55")
    assert result.bbox[2] == Decimal("23.69")
    assert result.bbox[3] == Decimal("37.62")

    assert len(result.alternative_paths) == 1
    alternative_path = result.alternative_paths[0]
    assert alternative_path.calculated_route[0] == Point(
        lat=Decimal("42.500"),
        lon=Decimal("47.8"))
    assert alternative_path.calculated_route[1] == Point(
        lat=Decimal("52.500"),
        lon=Decimal("57.8"))
    assert alternative_path.distance == Decimal("700.34")
    assert len(alternative_path.routing_points_on_route) == 2
    assert alternative_path.routing_points_on_route[0] == PointsOnRoute(
        is_hra=True,
        is_seca=False,
        distance=Decimal("4500.5"),
        distance_to_enter=Decimal("500.85"),
        heading=200,
        editable=False,
        name="Gibraltar",
        is_shown=True,
        delay_mins=False,
        center_point=Point(
            lat=Decimal("42.500"),
            lon=Decimal("47.8"),
        ),
    )
    assert alternative_path.routing_points_on_route[1] == PointsOnRoute(
        is_hra=True,
        is_seca=False,
        distance=Decimal("5500.5"),
        distance_to_enter=Decimal("600.85"),
        heading=100,
        editable=True,
        name="Gela",
        is_shown=False,
        delay_mins=True,
        center_point=Point(
            lat=Decimal("52.500"),
            lon=Decimal("57.8"),
        ),
    )
    assert alternative_path.piracy_distance == Decimal("1000.45")
    assert alternative_path.seca_distance == Decimal("800.89")
