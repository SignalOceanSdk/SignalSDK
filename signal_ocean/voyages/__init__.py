"""Voyages API Package.

Classes:
    VoyagesAPI: Represents Signal's Voyages API.
    Voyage: Represents a Voyage of a vessel.
    VoyageEvent: Represents an Event associated with a Voyage.
    VoyageEventDetail: Represents details about a VoyageEvent.
    VoyageGeo: Represents a geo asset object associated with a voyage.
    VoyagesFlat: Voyages with additional information in flat format.
    VoyagesIncremental: Incremental voyages, including token for next request.
    VoyagesCondensed: Voyages with additional information in condensed format.
    Vessel: Vessel name and IMO
    VesselFilter: Vessel Filter object
    VesselClass: Vessel class
    VesselClassFilter: Vessel class Filter object
    VesselType: Vessel type object
    VesselTypeFilter: Vessel type Filter object
"""

from .models import (
    Voyage,
    VoyageEvent,
    VoyageEventDetail,
    VoyageGeo,
    Vessel,
    VesselClass,
    VesselType,
    VesselFilter,
    VesselClassFilter,
    VesselTypeFilter,
    VoyageCondensed,
)
from .voyages_api import VoyagesAPI

__all__ = [
    "Voyage",
    "VoyageEvent",
    "VoyageEventDetail",
    "VoyageGeo",
    "VoyagesAPI",
    "Vessel",
    "VesselFilter",
    "VesselClass",
    "VesselClassFilter",
    "VesselType",
    "VesselTypeFilter",
    "VoyageCondensed",
]
