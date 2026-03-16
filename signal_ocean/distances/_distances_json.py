from typing import Mapping, cast, Any
from decimal import Decimal
from .models import RouteResponse, AlternativePath, PointsOnRoute, Point
from .._internals import as_decimal

JsonObject = Mapping[str, Any]


def parse_route_response(json: JsonObject) -> RouteResponse:
    return RouteResponse(
        id=cast(int, json.get("id")),
        start_point=parse_point(cast(JsonObject, json.get("startPoint"))),
        end_point=parse_point(cast(JsonObject, json.get("endPoint"))),
        calculated_route=tuple(
            parse_point(cast(JsonObject, cr))
            for cr in json.get("calculatedRoute", [])
        ),
        routing_points_on_route=tuple(
            parse_points_on_route(cast(JsonObject, rp))
            for rp in json.get("routingPointsOnRoute", [])
        ),
        distance=cast(Decimal, as_decimal(json.get("distance"))),
        piracy_distance=cast(Decimal, as_decimal(json.get("piracyDistance"))),
        seca_distance=cast(Decimal, as_decimal(json.get("secaDistance"))),
        alternative_paths=tuple(
            parse_alternative_path(cast(JsonObject, ap))
            for ap in json.get("alternativePaths", [])
        ),
        is_empty=cast(bool, json.get("isEmpty")),
        bbox=tuple(
            cast(Decimal, as_decimal(bbox))
            for bbox in json.get("bBox", [])
        ) if json.get("bBox", []) else None,
    )


def parse_alternative_path(json: JsonObject) -> AlternativePath:
    return AlternativePath(
        calculated_route=tuple(
            parse_point(cast(JsonObject, cr))
            for cr in json.get("calculatedRoute", [])
        ),
        distance=cast(Decimal, as_decimal(json.get("distance"))),
        routing_points_on_route=tuple(
            parse_points_on_route(cast(JsonObject, rp))
            for rp in json.get("routingPointsOnRoute", [])
        ),
        piracy_distance=cast(Decimal, as_decimal(json.get("piracyDistance"))),
        seca_distance=cast(Decimal, as_decimal(json.get("secaDistance"))),
    )


def parse_points_on_route(json: JsonObject) -> PointsOnRoute:
    return PointsOnRoute(
        is_hra=cast(bool, json.get("isHra")),
        is_seca=cast(bool, json.get("isSeca")),
        distance=cast(Decimal, as_decimal(json.get("distance"))),
        distance_to_enter=cast(Decimal, as_decimal(json.get("distanceToEnter"))),
        heading=cast(int, json.get("heading")),
        editable=cast(bool, json.get("editable")),
        name=cast(str, json.get("name")),
        is_shown=cast(bool, json.get("isShown")),
        delay_mins=cast(bool, json.get("delayMins")),
        center_point=parse_point(cast(JsonObject, json.get("centerPoint"))),
    )


def parse_point(json: JsonObject) -> Point:
    return Point(
        lat=cast(Decimal, as_decimal(json.get("lat"))),
        lon=cast(Decimal, as_decimal(json.get("lon"))),
    )
