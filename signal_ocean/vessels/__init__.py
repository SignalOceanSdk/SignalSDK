"""Vessels API Package.

Classes:
    VesselsAPI: Represents Signal's Vessels API.
    Vessel: Represents a Vessel.
    VesselType: Represents the type of the vessel.
    VesselClass: Represents the class of the vessel.
"""

from .models import Vessel, VesselType, VesselClass
from .vessels_api import VesselsAPI

__all__ = ["Vessel", "VesselType", "VesselClass", "VesselsAPI"]
