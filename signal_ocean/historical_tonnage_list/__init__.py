"""Historical Tonnage List API Package.

Classes:
    HistoricalTonnageListAPI: Represents Signal's Historical Tonnage List API.

    HistoricalTonnageList: Result of a Historical Tonnage List query.

    TonnageList: A singular tonnage list in HistoricalTonnageList.

    Vessel: A vessel contained in a TonnageList.

    VesselFilter: Used for filtering vessels in queries.

    PushType: Contains constants for available push types.

    MarketDeployment: Contains constants for available market deployments.

    CommercialStatus: Contains constants for available commercial statuses.

    VesseSubclass: Contains constants for available vessel subclasses.

    LocationTaxonomy: Contains constants for available location taxonomies.

    Area: A geographical area.

    Column: Contains constants for available data frame column names.

    IndexLevel: Contains constants for available data frame index levels.

    OperationalStatus: Contains constants for available operational statuses.

    FixtureType: Contains constants for available fixture types.
"""
import warnings

from .historical_tonnage_list_api import HistoricalTonnageListAPI
from .historical_tonnage_list import HistoricalTonnageList
from .tonnage_list import TonnageList
from .vessel import Vessel
from .vessel_filter import VesselFilter
from .push_type import PushType
from .market_deployment import MarketDeployment
from .commercial_status import CommercialStatus
from .vessel_subclass import VesselSubclass
from .location_taxonomy import LocationTaxonomy
from .area import Area
from .column import Column
from .index_level import IndexLevel
from .operational_status import OperationalStatus
from .fixture_type import FixtureType

warnings.warn(
    "The historical_tonnage_list package is deprecated and will be removed in "
    "a future version of the SDK. Please use the tonnage_list package "
    "instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "HistoricalTonnageListAPI",
    "HistoricalTonnageList",
    "TonnageList",
    "Vessel",
    "VesselFilter",
    "PushType",
    "MarketDeployment",
    "CommercialStatus",
    "VesselSubclass",
    "LocationTaxonomy",
    "Area",
    "Column",
    "IndexLevel",
    "OperationalStatus",
    "FixtureType",
]
