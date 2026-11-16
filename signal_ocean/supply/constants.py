"""Names the Supply API accepts in its enumerated filter fields.

Every value is the exact name that the API expects. Filters also accept
plain strings, so names that the API adds later work without an SDK release.
"""
from .._internals import IterableConstants


class VesselType(metaclass=IterableConstants):
    """Vessel types, for `vessel_type`."""

    TANKER = "Tanker"
    DRY = "Dry"
    LNG = "LNG"
    LPG = "LPG"


class VesselClass(metaclass=IterableConstants):
    """Vessel classes, for `vessel_class`."""

    VLCC = "VLCC"
    SUEZMAX = "Suezmax"
    AFRAMAX = "Aframax"
    PANAMAX_TANKER = "PanamaxTanker"
    MR2 = "MR2"
    MR1 = "MR1"
    SMALL = "Small"
    VLOC = "VLOC"
    CAPESIZE = "Capesize"
    POST_PANAMAX_DRY = "PostPanamaxDry"
    PANAMAX_DRY = "PanamaxDry"
    SUPRAMAX = "Supramax"
    HANDYMAX = "Handymax"
    HANDYSIZE = "Handysize"
    SMALL_DRY = "SmallDry"
    LNG = "LNGLng"
    VLGC_LPG = "VLGCLpg"
    MIDSIZE_LPG = "MidsizeLpg"
    HANDY_LPG = "HandyLpg"
    SMALL_LPG = "SmallLpg"


class DefiningSize(metaclass=IterableConstants):
    """Size units, for `defining_size`."""

    DEADWEIGHT = "Deadweight"
    CUBIC_SIZE = "CubicSize"


class VesselSubclass(metaclass=IterableConstants):
    """Vessel subclasses, for `vessel_subclass`."""

    CRUDE = "Crude"
    PRODUCT = "Product"
    CHEMICAL = "Chemical"
    BULK = "Bulk"
    GENERAL_CARGO = "GeneralCargo"
    REFRIGERATED = "Refrigerated"
    PRESSURIZED = "Pressurized"
    SEMI_PRESSURIZED = "SemiPressurized"
    VLEC = "Vlec"


class AvailabilityState(metaclass=IterableConstants):
    """Commercial availability states, for `availability_state`."""

    ON_SUBS = "OnSubs"
    FULLY_FIXED = "FullyFixed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    AVAILABLE = "Available"
    POTENTIALLY_FIXED = "PotentiallyFixed"


class MarketStatus(metaclass=IterableConstants):
    """Market push states, for `market_status`."""

    NOT_PUSHED = "NotPushed"
    POSS_PUSHED = "PossPushed"
    PUSHED = "Pushed"


class MarketDeployment(metaclass=IterableConstants):
    """Market deployment types, for `market_deployment`."""

    SPOT = "Spot"
    PROGRAM = "Program"
    RELET = "Relet"
    CONTRACT = "Contract"


class PositionSourceOrigin(metaclass=IterableConstants):
    """Position data origins, for `position_source_origin`."""

    NONE = "None"
    MANUAL = "Manual"
    LATEST_POSITION = "LatestPosition"
    SYSTEM = "System"


class PositionSourceType(metaclass=IterableConstants):
    """Position data origin types, for `position_source_type`."""

    NONE = "None"
    MODEL_PREDICTION = "ModelPrediction"
    EMAIL = "Email"
    SLACK = "Slack"
    WHATS_APP = "WhatsApp"
    TEAMS = "Teams"
    DATA_PREDICTION = "DataPrediction"


class VoyageState(metaclass=IterableConstants):
    """Operational voyage states, for `voyage_state`."""

    BALLAST_FIXED = "BallastFixed"
    REPAIRS = "Repairs"
    WAIT_TO_LOAD = "WaitToLoad"
    LOADING = "Loading"
    LADEN = "Laden"
    WAIT_TO_DISCHARGE = "WaitToDischarge"
    DISCHARGING = "Discharging"
    ACTIVE_STORAGE = "ActiveStorage"
    BALLAST_FIXED_IMPLIED = "BallastFixedImplied"
    BALLAST_UNFIXED = "BallastUnfixed"


class EtaCalculationBasis(metaclass=IterableConstants):
    """Start position and date of an ETA calculation."""

    DEFAULT = "Default"
    LATEST_OPEN_DATE = "LatestOpenDate"
    EARLIEST_OPEN_DATE = "EarliestOpenDate"
    LATEST_AIS_LOCATION = "LatestAisLocation"


class Restrictions(metaclass=IterableConstants):
    """Routing restrictions of a live ETA calculation."""

    NONE = "None"
    MESSINA = "Messina"
    ORESUND = "Oresund"
    PANAMA = "Panama"
    SUEZ = "Suez"
    SUEZ_OPEN_ONLY_NORTH_BOUND = "SuezOpenOnlyNorthBound"
    ALL = "All"


class Coating(metaclass=IterableConstants):
    """Tank coating types, for `coating`."""

    NONE = "None"
    STS_T_COATING = "StsTCoating"
    EPOXY_COATING = "EpoxyCoating"
    ZINC_COATING = "ZincCoating"
    MARINELINE_COATING = "MarinelineCoating"
    INTERLINE_COATING = "InterlineCoating"
    NO_COATING = "NoCoating"


class ImoType(metaclass=IterableConstants):
    """IMO ship types, for `imo_type`."""

    NONE = "None"
    TYPE1 = "Type1"
    TYPE2 = "Type2"
    TYPE3 = "Type3"
    NO_IMO_TYPE = "NoImoType"


class LocationTaxonomy(metaclass=IterableConstants):
    """Location levels, for `GeoLocation.location_taxonomy`."""

    GEO_ASSET = 1
    PORT = 2
    COUNTRY = 3
    LEVEL0 = 4
    LEVEL1 = 5
