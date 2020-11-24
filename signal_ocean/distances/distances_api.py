# noqa: D100


from typing import Tuple, Optional

from .. import Connection
from .port import Port
from .port_filter import PortFilter
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter
from .loading_condition import LoadingCondition
from decimal import Decimal
from . import _distances_json
from .._internals import as_decimal
from .models import RouteResponse


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
            "api/v1/vessel-classes"
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
            "api/v1/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

    def get_loading_conditions(
        self
    ) -> Tuple[LoadingCondition, ...]:
        """Retrieves available loading conditions.

        Returns:
            A tuple of available loading conditions.
        """
        response = self.__connection._make_get_request(
            "api/v1/LoadingConditions"
        )
        response.raise_for_status()

        loadingconditions = (LoadingCondition(**p) for p in response.json())

        return tuple(loadingconditions)

    def get_point_to_point_distance(self,
                                    vessel_class_id: int,
                                    loading_condition_id: int,
                                    latitude_from: Decimal,
                                    latitude_to: Decimal,
                                    longitude_from: Decimal,
                                    longitude_to: Decimal
                                    ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            latitude_from: The starting point latitude for the distance
                route calculation.
            latitude_to: The ending point latitude for the distance route
                calculation.
            longitude_from: The starting point longitude for the distance
                route calculation.
            longitude_to: The ending point longitude for the distance route
                calculation.

        Returns:
            A Decimal representing the distance in NM between two points.
        """

        endpoint = "/api/v1/Distance/PointToPoint"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&latitudefrom={latitude_from}"
        endpoint += f"&latitudeto={latitude_to}"
        endpoint += f"&longitudefrom={longitude_from}"
        endpoint += f"&longitudeto={longitude_to}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_point_to_port_distance(self,
                                   vessel_class_id: int,
                                   loading_condition_id: int,
                                   latitude: Decimal,
                                   longitude: Decimal,
                                   port_id: int
                                   ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            latitude: The starting point latitude for the distance
                route calculation.
            longitude_from: The starting point longitude for the distance
                route calculation.
            port_id: The ending port for the distance
                route calculation.

        Returns:
            A Decimal representing the distance in NM between a point
                and a port.
        """

        endpoint = "/api/v1/Distance/PointToPort"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&latitude={latitude}"
        endpoint += f"&longitude={longitude}"
        endpoint += f"&portid={port_id}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_port_to_port_distance(self,
                                  vessel_class_id: int,
                                  loading_condition_id: int,
                                  port_id_from: int,
                                  port_id_to: int
                                  ) -> Optional[Decimal]:
        """Retrieves the distance from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            port_id_from: The starting port for the distance
                route calculation.
            port_id_to: The ending port for the distance
                route calculation.

        Returns:
            A Decimal representing the distance in NM between two ports.
        """

        endpoint = "/api/v1/Distance/PortToPort"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&portIdFrom={port_id_from}"
        endpoint += f"&portIdTo={port_id_to}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return as_decimal(response.json())

    def get_point_to_point_route(self,
                                 vessel_class_id: int,
                                 loading_condition_id: int,
                                 latitude_from: Decimal,
                                 latitude_to: Decimal,
                                 longitude_from: Decimal,
                                 longitude_to: Decimal
                                 ) -> Optional[RouteResponse]:
        """Retrieves the route from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            latitude_from: The starting point latitude for the distance
                route calculation.
            latitude_to: The ending point latitude for the distance route
                calculation.
            longitude_from: The starting point longitude for the distance
                route calculation.
            longitude_to: The ending point longitude for the distance route
                calculation.

        Returns:
            A Route between two points with distance in NM.
        """

        endpoint = "/api/v1/Distance/PointToPoint/Route"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&latitudefrom={latitude_from}"
        endpoint += f"&latitudeto={latitude_to}"
        endpoint += f"&longitudefrom={longitude_from}"
        endpoint += f"&longitudeto={longitude_to}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())

    def get_point_to_port_route(self,
                                vessel_class_id: int,
                                loading_condition_id: int,
                                latitude: Decimal,
                                longitude: Decimal,
                                port_id: int
                                ) -> Optional[RouteResponse]:
        """Retrieves the route from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            latitude: The starting point latitude for the distance
                route calculation.
            longitude_from: The starting point longitude for the distance
                route calculation.
            port_id: The ending port for the distance
                route calculation.

        Returns:
            A Route between a point and a port with distance in NM.
        """

        endpoint = "/api/v1/Distance/PointToPort/Route"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&latitude={latitude}"
        endpoint += f"&longitude={longitude}"
        endpoint += f"&portid={port_id}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())

    def get_port_to_port_route(self,
                               vessel_class_id: int,
                               loading_condition_id: int,
                               port_id_from: int,
                               port_id_to: int
                               ) -> Optional[RouteResponse]:
        """Retrieves the route from one point to another.

        Args:
            vessel_class_id: Vessel class for which the distance will be
                calculated.
            loading_condition_id: Loading condition for which the distance
                will be calculated.
            port_id_from: The starting port for the distance
                route calculation.
            port_id_to: The ending port for the distance
                route calculation.

        Returns:
            A Route between two ports with distance in NM.
        """

        endpoint = "/api/v1/Distance/PortToPort/Route"
        endpoint += f"?vesselclass={vessel_class_id}"
        endpoint += f"&loadingcondition={loading_condition_id}"
        endpoint += f"&portIdFrom={port_id_from}"
        endpoint += f"&portIdTo={port_id_to}"

        response = self.__connection._make_get_request(
            endpoint
        )

        response.raise_for_status()

        return _distances_json.parse_route_response(response.json())
