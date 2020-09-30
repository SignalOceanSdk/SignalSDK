# noqa: D100

from .._internals import IterableConstants


class OperationalStatus(metaclass=IterableConstants):
    """Contains constants for available operational statuses."""
    BALLAST_FIXED = "Ballast Fixed"
    REPAIRS = "Repairs"
    WAITING_TO_LOAD = "Waiting to Load"
    LOADING = "Loading"
    LADEN = "Laden"
    WAITING_TO_DISCHARGE = "Waiting to Discharge"
    DISCHARGING = "Discharging"
    ACTIVE_STORAGE = "Active Storage"
    BALLAST_UNFIXED = "Ballast Unfixed"
    BALLAST_FIXED_IMPLIED = "Ballast Fixed (implied)"
