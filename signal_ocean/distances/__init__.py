"""Distances API Package.

Classes:
    DistancesAPI: Represents Signal's Distances API.

    VesselClass: A group of vessels of similar characteristics.

    VesselClassFilter: A filter used to find specific vessel classes.

    Port: A maritime facility where vessels can dock.

    PortFilter: A filter used to find specific ports.

    LoadingCondition: The states of a vessel carrying cargo.

    RouteResponse: A route between two points

    AlternativePath: An alternative path for the route

    PointsOnRoute: A point and extra properties needed for a route

    Point: A point in latitude and longitude.

"""

from .distances_api import DistancesAPI
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter
from .port import Port
from .port_filter import PortFilter
from .loading_condition import LoadingCondition
from .models import (
    RouteResponse,
    AlternativePath,
    PointsOnRoute,
    Point,
    RouteRestrictions,
)

__all__ = [
    "DistancesAPI",
    "VesselClass",
    "VesselClassFilter",
    "Port",
    "PortFilter",
    "LoadingCondition",
    "RouteResponse",
    "AlternativePath",
    "PointsOnRoute",
    "Point",
    "RouteRestrictions",
]
