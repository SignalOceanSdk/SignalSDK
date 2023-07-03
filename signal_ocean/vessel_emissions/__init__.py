"""Vessel Emissions API Package.

Classes:
    VesselEmissionsAPI: Represents Signal's Vessel Emissions API.
    EmissionsEstimation: Represents Emissions Estimation for a single Voyage.
    Metrics: Represents Emissions Metrics for a Vessel.
    VesselClassEmissions: Represents Emissions Estimation
    for a all available vessels of a vessel class.
    VesselClassMetrics: Represents Emissions Metrics
    for a all available vessels of a vessel class

"""

from .models import (
    VesselClassMetrics,
    VesselClassEmissions,
    EmissionsEstimation,
    Metrics
)
from .vessel_emissions_api import VesselEmissionsAPI

__all__ = [
    "Metrics",
    "EmissionsEstimation",
    "VesselClassMetrics",
    "VesselClassEmissions",
    "VesselEmissionsAPI"
]
