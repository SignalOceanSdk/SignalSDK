# noqa: D100

from decimal import Decimal
from typing import Tuple, Optional, Dict

from signal_ocean.util.pydantic_base import SignalBaseModel


class Point(SignalBaseModel):
    """A point on the surface of Earth.

    Attributes:
        lat: The latitude of the point.
        lon: The longitude of the point.
    """

    lat: Optional[Decimal] = None
    lon: Optional[Decimal] = None


class PointsOnRoute(SignalBaseModel):
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

    is_hra: Optional[bool] = None
    is_seca: Optional[bool] = None
    distance: Optional[Decimal] = None
    distance_to_enter: Optional[Decimal] = None
    heading: Optional[int] = None
    editable: Optional[bool] = None
    name: Optional[str] = None
    is_shown: Optional[bool] = None
    delay_mins: Optional[int] = None
    center_point: Optional[Point] = None


class AlternativePath(SignalBaseModel):
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

    calculated_route: Optional[Tuple[Point, ...]] = None
    distance: Optional[Decimal] = None
    routing_points_on_route: Optional[Tuple[PointsOnRoute, ...]] = None
    piracy_distance: Optional[Decimal] = None
    seca_distance: Optional[Decimal] = None


class RouteResponse(SignalBaseModel):
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

    id: Optional[int] = None
    start_point: Optional[Point] = None
    end_point: Optional[Point] = None
    calculated_route: Optional[Tuple[Point, ...]] = None
    routing_points_on_route: Optional[Tuple[PointsOnRoute, ...]] = None
    distance: Optional[Decimal] = None
    piracy_distance: Optional[Decimal] = None
    seca_distance: Optional[Decimal] = None
    alternative_paths: Optional[Tuple[AlternativePath, ...]] = None
    is_empty: Optional[bool] = None
    bbox: Optional[Tuple[Decimal, ...]] = None


class RouteRestrictions(SignalBaseModel):
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
