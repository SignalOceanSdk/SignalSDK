"""Vessel Valuations API Package.

Classes:
    VesselValuationsAPI: Represents Signal's Vessel Valuations API.
    ValuationSummary: A short summary of a specific vessel's valuation.
    ValuationHistory: A history of valuations for a specific vessel.
"""

from .vessel_valuations_api import VesselValuationsAPI
from .models import ValuationHistory, ValuationSummary
