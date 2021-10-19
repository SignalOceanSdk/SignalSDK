"""Freight Rates API Package.

Classes:
    FreightRatesAPI: Represents Signal's Freight Rates API.

    FreightPricing: The freight pricing given a load and discharge port.

    VesselClass: A vessel class.

    Port: A maritime facility where vessels can dock.

    PortFilter: A filter used to find specific ports.

"""

from .models import FreightPricing, Port, Cost
from .freight_rates_api import FreightRatesAPI
from .port_filter import PortFilter

__all__ = ["FreightPricing", "Port", "Cost", "FreightRatesAPI",
           "PortFilter"]
