# noqa: D100

from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple, Optional, Dict


@dataclass(frozen=True)
class Point:
    """A point on the surface of Earth.

    Attributes:
        lat: The latitude of the point.
        lon: The longitude of the point.
    """

    lat: Decimal
    lon: Decimal


@dataclass(frozen=True)
class PointsOnRoute:
    """A point and extra properties needed for a route.

    Attributes:
        is_hra: Is the point in a high-risk area.
        is_seca: Is the point in a Sulfur Emission Control Area.
        distance: The distance between the two points.
        distance_to_enter:
        heading: The point on route heading.
        editable: If the point on route is editable.
        name: The point on route name.
        is_shown: If the point on route is shown.
        delay_mins: The delay in minutes.
        center_point: The center point of route.
    """

    is_hra: bool
    is_seca: bool
    distance: Decimal
    distance_to_enter: Decimal
    heading: int
    editable: bool
    name: str
    is_shown: bool
    delay_mins: int
    center_point: Point


@dataclass(frozen=True)
class AlternativePath:
    """An alternative path for the route.

    Attributes:
        calculated_route: List of coordinates between start and end point.
        distance: The distance between the two points.
        routing_points_on_route:
        piracy_distance: The distance between the two points when piracy
            is considered.
        seca_distance: The distance between the two points when SECA is
            considered.
    """

    calculated_route: Tuple[Point, ...]
    distance: Decimal
    routing_points_on_route: Tuple[PointsOnRoute, ...]
    piracy_distance: Decimal
    seca_distance: Decimal


@dataclass(frozen=True)
class RouteResponse:
    """A route between two points.

    Attributes:
        id: The id of the route response.
        start_point: Start point coordinates.
        end_point: End point coordinates.
        calculated_route: List of coordinates between start and end point.
        routing_points_on_route: List of points on a route.
        distance: The distance between the two points.
        piracy_distance: The distance between the two points when piracy is
            considered.
        seca_distance: The distance between the two points when seca is
            considered.
        alternative_paths: List of alternative paths between the two points.
        is_empty: If the response is empty.
        bbox: The bounding box of the route.
    """

    id: int
    start_point: Point
    end_point: Point
    calculated_route: Tuple[Point, ...]
    routing_points_on_route: Tuple[PointsOnRoute, ...]
    distance: Decimal
    piracy_distance: Decimal
    seca_distance: Decimal
    alternative_paths: Tuple[AlternativePath, ...]
    is_empty: bool
    bbox: Optional[Tuple[Decimal, ...]]


@dataclass(frozen=True)
class RouteRestrictions:
    """Restrictions that can be placed upon a route.

    Attributes:
        is_suez_open: Determines whether or not to route through the Suez
            Canal.
        is_panama_open: Determines whether or not to route through the Panama
            Canal.
        is_messina_open: Determines whether or not to route through the Strait
            of Messina.
        is_oresund_open: Determines whether or not to route through the Øresund
            Strait.
        is_suez_open_only_northbound: Determines whether or not to route
            through the Suez Canal only when northbound.
        is_piracy_considered: Determines whether or not to route through areas
            where a piracy threat exists.
        minimize_seca: Determines whether or not to minimize distance travelled
            through SECA areas.
    """

    is_suez_open: Optional[bool] = None
    is_panama_open: Optional[bool] = None
    is_messina_open: Optional[bool] = None
    is_oresund_open: Optional[bool] = None
    is_suez_open_only_northbound: Optional[bool] = None
    is_piracy_considered: Optional[bool] = None
    minimize_seca: Optional[bool] = None

    def _to_query_string(self) -> Dict[str, Optional[bool]]:
        return {
            "IsSuezOpen": self.is_suez_open,
            "IsPanamaOpen": self.is_panama_open,
            "IsPiracyConsidered": self.is_piracy_considered,
            "IsMessinaOpen": self.is_messina_open,
            "IsOresundOpen": self.is_oresund_open,
            "IsSuezOpenOnlyNorthbound": self.is_suez_open_only_northbound,
            "MinimizeSeca": self.minimize_seca,
        }
