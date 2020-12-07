from typing import Mapping, cast, Any
from decimal import Decimal
from .models import RouteResponse, AlternativePath, PointsOnRoute, Point
from .._internals import as_decimal

JsonObject = Mapping[str, Any]


def parse_route_response(json: JsonObject) -> RouteResponse:
    return RouteResponse(
        cast(int, json.get("id")),
        parse_point(cast(JsonObject, json.get("startPoint"))),
        parse_point(cast(JsonObject, json.get("endPoint"))),
        tuple(
            parse_point(cast(JsonObject, cr))
            for cr in json.get("calculatedRoute", [])
        ),
        tuple(
            parse_points_on_route(cast(JsonObject, rp))
            for rp in json.get("routingPointsOnRoute", [])
        ),
        cast(Decimal, as_decimal(json.get("distance"))),
        cast(Decimal, as_decimal(json.get("piracyDistance"))),
        cast(Decimal, as_decimal(json.get("secaDistance"))),
        tuple(
            parse_alternative_path(cast(JsonObject, ap))
            for ap in json.get("alternativePaths", [])
        ),
        cast(bool, json.get("isEmpty")),
        tuple(
            cast(Decimal, as_decimal(bbox))
            for bbox in json.get("bBox", [])
        ) if json.get("bBox", []) else None,
    )


def parse_alternative_path(json: JsonObject) -> AlternativePath:
    return AlternativePath(
        tuple(
            parse_point(cast(JsonObject, cr))
            for cr in json.get("calculatedRoute", [])
        ),
        cast(Decimal, as_decimal(json.get("distance"))),
        tuple(
            parse_points_on_route(cast(JsonObject, rp))
            for rp in json.get("routingPointsOnRoute", [])
        ),
        cast(Decimal, as_decimal(json.get("piracyDistance"))),
        cast(Decimal, as_decimal(json.get("secaDistance"))),
    )


def parse_points_on_route(json: JsonObject) -> PointsOnRoute:
    return PointsOnRoute(
        cast(bool, json.get("isHra")),
        cast(bool, json.get("isSeca")),
        cast(Decimal, as_decimal(json.get("distance"))),
        cast(Decimal, as_decimal(json.get("distanceToEnter"))),
        cast(int, json.get("heading")),
        cast(bool, json.get("editable")),
        cast(str, json.get("name")),
        cast(bool, json.get("isShown")),
        cast(bool, json.get("delayMins")),
        parse_point(cast(JsonObject, json.get("centerPoint"))),
    )


def parse_point(json: JsonObject) -> Point:
    return Point(
        cast(Decimal, as_decimal(json.get("lat"))),
        cast(Decimal, as_decimal(json.get("lon"))),
    )
