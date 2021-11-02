"""OilX Cargo Tracking API Package.

Classes:
    OilxCargoTrackingAPI: Represents Signal's OilX Cargo Tracking API.
    CargoFlow: Represents a CargoFlow.
    CargoFlowsPagedResponse:
        Represents paged response of OilX Cargo Tracking API.
"""
from .oilx_models import CargoFlow, CargoFlowsPagedResponse
from .oilx_cargo_tracking_api import OilxCargoTrackingAPI

__all__ = ["CargoFlow", "CargoFlowsPagedResponse", "OilxCargoTrackingAPI"]
