"""Vessel Consumptions API Package.

Classes:
    VesselConsumptionsAPI: Represents Signal's Vessel Consumptions API.
    VesselConsumptions: Represents vessel consumptions data.
    AdvertisedConsumptions: Represents advertised consumptions data.
    AdvertisedConsumptionsPage: Represents a page of advertised consumptions.

"""

from .models import (
    VesselConsumptions,
    AdvertisedConsumptions,
    AdvertisedConsumptionsPage,
)
from .vessel_consumptions_api import VesselConsumptionsAPI

__all__ = [
    "VesselConsumptions",
    "AdvertisedConsumptions",
    "AdvertisedConsumptionsPage",
    "VesselConsumptionsAPI",
]
