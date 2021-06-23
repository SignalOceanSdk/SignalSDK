"""Market Rates API Package.

Classes:
    MarketRatesAPI: Represents Signal's Market Rates API.

    MarketRate: The market rate of a certain route or vessel class.

    Route: A route with available market rate.

    VesselClass: A vessel class.

"""

from .models import MarketRate, Route, VesselClass
from .market_rates_api import MarketRatesAPI

__all__ = ["VesselClass", "Route", "MarketRate", "MarketRatesAPI"]
