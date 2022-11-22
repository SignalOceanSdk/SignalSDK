"""Market Rates API Package.

Classes:
    MarketRatesAPI: Represents Signal's Market Rates API.

    MarketRate: The market rate of a certain route or vessel class.

    Route: A route with available market rate.

    VesselClass: A vessel class.

    CargoId: The cargo ID, Dirty (0), Clean(1) or IMO (2).

"""

from .enums import CargoId
from .models import MarketRate, Route, VesselClass
from .market_rates_api import MarketRatesAPI

__all__ = ["VesselClass", "Route", "MarketRate", "MarketRatesAPI", "CargoId"]
