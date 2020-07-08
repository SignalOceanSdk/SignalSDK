from .._internals import IterableConstants


class OperationalStatus(metaclass=IterableConstants):
    BALLAST_FIXED = "Ballast Fixed"
    REPAIRS = "Repairs"
    WAITING_TO_LOAD = "Waiting to Load"
    LOADING = "Loading"
    LADEN = "Laden"
    WAITING_TO_DISCHARGE = "Waiting to Discharge"
    DISCHARGING = "Discharging"
    ACTIVE_STORAGE = "Active Storage"
    BALLAST_UNFIXED = "Ballast Unfixed"
