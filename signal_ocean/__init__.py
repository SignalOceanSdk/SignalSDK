"""The top-level Signal SDK package.

Contains classes common across all submodules and used across APIs.

Classes:
    Connection: Facilitates authenticated communication with Signal APIs.
    Port: A maritime facility where vessels can dock.
    PortAPI: An API used to fetch port data.
    PortFilter: A filter that used to find specific ports.
    VesselClass: A group of vessels of similar characteristics.
    VesselClassAPI: An API used to fetch available vessel classes.
    VesselClassFilter: A filter used to find specific vessel classes.
"""

from .connection import Connection
from .market_rates import MarketRatesAPI
from .freight_rates import FreightRatesAPI
from .port import Port
from .port_api import PortAPI
from .port_expenses import PortExpensesAPI
from .port_filter import PortFilter
from .vessel_class import VesselClass
from .vessel_class_api import VesselClassAPI
from .vessel_class_filter import VesselClassFilter

__all__ = [
    "Connection",
    "Port",
    "PortAPI",
    "PortExpensesAPI",
    "MarketRatesAPI",
    "FreightRatesAPI",
    "PortFilter",
    "VesselClass",
    "VesselClassAPI",
    "VesselClassFilter",
]
