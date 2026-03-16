from datetime import datetime
from typing import cast, Mapping, Any, List, Tuple

from .models import Route, MarketRate


def parse_market_rates(json: List[Mapping[str, Any]]) -> \
        Tuple[MarketRate, ...]:
    rates: List[MarketRate] = []
    for rate_json in json:
        if rate_json.get("RouteId") == "TC1" and \
                rate_json.get("VesselClassId") == 86:
            continue
        rate = MarketRate(
            route_id=cast(str, rate_json.get("RouteId")),
            rate_date=cast(datetime, rate_json.get("RateDate")),
            rate_value=cast(float, rate_json.get("RateValue")),
            unit=cast(str, rate_json.get("Unit")),
            vessel_class_id=cast(int, rate_json.get("VesselClassId")),
            deprecated_to=cast(str, rate_json.get("DeprecatedTo")),
        )
        rates.append(rate)
    return tuple(rates)


def parse_routes(json: List[Mapping[str, Any]]) -> Tuple[Route, ...]:
    routes: List[Route] = []
    for route_json in json:
        route = Route(
            id=cast(str, route_json.get("route_id")),
            description=cast(str, route_json.get("description")),
            unit=cast(str, route_json.get("unit")),
            vessel_class_id=cast(int, route_json.get("vessel_class_id")),
            cargo_id=cast(int, route_json.get("cargo_id")),
            load_port_id=cast(int, route_json.get("load_port_id")),
            discharge_port_id=cast(
                int, route_json.get("discharge_port_id")
            ),
            load_area_id=cast(
                int, route_json.get("load_area_id")
            ),
            discharge_area_id=cast(
                int, route_json.get("discharge_area_id")
            ),
            load_port_2_id=cast(
                int, route_json.get("load_port_2_id")
            ),
            discharge_port_2_id=cast(
                int,
                route_json.get("discharge_port_2_id")
            ),
            load_area_2_id=cast(
                int, route_json.get("load_area_2_id")
            ),
            discharge_area_2_id=cast(
                int,
                route_json.get("discharge_area_2_id")
            ),
            deprecated_to=cast(str, route_json.get("deprecated_to")),
            deprecated_since=cast(
                datetime,
                route_json.get("deprecated_since")
            ),
        )
        routes.append(route)
    return tuple(routes)
