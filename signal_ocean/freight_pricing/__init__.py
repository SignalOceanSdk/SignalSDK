"""Freight Pricing API Package.

Classes:
    FreightPricingAPI: Represents Signal's Freight Pricing API.
    VesselType: An enumeration of available vessel types.
    VesselSubclass: An enumeration of available vessel subclasses.
    FreightPricingItem: Freight pricing information for a specific vessel class.
    FreightPricing: A collection of freight pricing items per vessel class.
"""

from .freight_pricing_api import FreightPricingAPI
from .vessel_type import VesselType
from .vessel_subclass import VesselSubclass
from .freight_pricing import FreightPricing, FreightPricingItem
