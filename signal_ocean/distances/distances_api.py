# noqa: D100

from typing import Tuple, Optional
from datetime import date
from decimal import Decimal

from .. import Connection
from .port import Port
from .port_filter import PortFilter
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter
from . import _distances_json
from .._internals import as_decimal, format_iso_date
from .models import RouteResponse, Point, RouteRestrictions


class DistancesAPI:
    """Represents Signal's Distances API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes DistancesAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_vessel_classes(
        self, class_filter: Optional[VesselClassFilter] = None
    ) -> Tuple[VesselClass, ...]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If not
                specified, returns all available vessel classes.

        Returns:
            A tuple of available vessel classes that match the filter.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/VesselClasses"
        )
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))

    def get_ports(
        self, port_filter: Optional[PortFilter] = None
    ) -> Tuple[Port, ...]:
        """Retrieves available ports.

        Args:
            port_filter: A filter used to find specific ports. If not
                specified, returns all available ports.

        Returns:
            A tuple of available ports that match the filter.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

    def get_point_to_point_distance(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        start_point: Point,
        end_point: Point,
    ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            start_point: The starting point latitude and longitude.
            end_point: The ending point latitude and longitude.

        Returns:
            A Decimal representing the distance in NM between two points.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PointToPoint",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "latitudefrom": str(start_point.lat),
                "latitudeto": str(end_point.lat),
                "longitudefrom": str(start_point.lon),
                "longitudeto": str(end_point.lon),
            },
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_point_to_port_distance(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        point: Point,
        port: Port,
    ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            point: The starting point latitude and longitude.
            port: The target port.

        Returns:
            A Decimal representing the distance in NM between a point
                and a port.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PointToPort",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "latitude": str(point.lat),
                "longitude": str(point.lon),
                "portid": port.id,
            },
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_port_to_port_distance(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        port_from: Port,
        port_to: Port,
    ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            port_from: The starting port for the distance
                route calculation.
            port_to: The ending port for the distance
                route calculation.

        Returns:
            A Decimal representing the distance in NM between two ports.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PortToPort",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "portIdFrom": port_from.id,
                "portIdTo": port_to.id,
            },
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_point_to_point_route(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        start_point: Point,
        end_point: Point,
    ) -> RouteResponse:
        """Retrieves the route from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            start_point: The starting point latitude and longitude.
            end_point: The ending point latitude and longitude.

        Returns:
            A Route between two points with distance in NM.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PointToPoint/Route",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "latitudefrom": str(start_point.lat),
                "latitudeto": str(end_point.lat),
                "longitudefrom": str(start_point.lon),
                "longitudeto": str(end_point.lon),
            },
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())

    def get_point_to_port_route(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        point: Point,
        port: Port,
    ) -> RouteResponse:
        """Retrieves the route from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            point: The starting point latitude and longitude.
            port: The ending port for the distance
                route calculation.

        Returns:
            A Route between a point and a port with distance in NM.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PointToPort/Route",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "latitude": str(point.lat),
                "longitude": str(point.lon),
                "portid": port.id,
            },
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())

    def get_port_to_port_route(
        self,
        vessel_class: VesselClass,
        loading_condition_id: int,
        port_from: Port,
        port_to: Port,
    ) -> RouteResponse:
        """Retrieves the route from one point to another.

        Args:
            vessel_class: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition of the vessels
                for which the distance will be calculated.
                Options available: Laden and Ballast.
            port_from: The starting port for the distance
                route calculation.
            port_to: The ending port for the distance
                route calculation.

        Returns:
            A Route between two ports with distance in NM.
        """
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/PortToPort/Route",
            {
                "vesselclass": vessel_class.id,
                "loadingcondition": loading_condition_id,
                "portIdFrom": port_from.id,
                "portIdTo": port_to.id,
            },
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())

    def get_generic_point_to_point_route(
        self,
        start_point: Point,
        end_point: Point,
        route_restrictions: Optional[RouteRestrictions] = None,
        delays_valid_at: Optional[date] = None,
        get_alternatives: Optional[bool] = None,
    ) -> RouteResponse:
        """Retrieves a generic route between two points.

        The method takes into consideration the provided restrictions and can
        also return alternative routes.

        Args:
            start_point: The starting point latitude and longitude.
            end_point: The ending point latitude and longitude.
            route_restrictions: Restrictions to obey while calculating the
                route.
            delays_valid_at: Date at which the route delays are valid.
            get_alternatives: Whether or not to include alternative routes.

        Returns:
            A Route between two points with distance in NM.
        """
        route_restrictions = route_restrictions or RouteRestrictions()
        response = self.__connection._make_get_request(
            "/distances-api/api/v1/Distance/Generic",
            {
                "StartPointLatitude": str(start_point.lat),
                "StartPointLongitude": str(start_point.lon),
                "EndPointLatitude": str(end_point.lat),
                "EndPointLongitude": str(end_point.lon),
                "DelaysValidAt": format_iso_date(delays_valid_at)
                if delays_valid_at
                else None,
                "GetAlternatives": get_alternatives,
                **route_restrictions._to_query_string(),
            },
        )

        response.raise_for_status()
        return _distances_json.parse_route_response(response.json())
