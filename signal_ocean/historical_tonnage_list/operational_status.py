# noqa: D100

from .._internals import IterableConstants


class OperationalStatus(metaclass=IterableConstants):
    """Contains constants for available operational statuses."""
    BALLAST_FIXED = "Ballast Fixed"
    '''
    Vessel is currently empty of cargo but fixed forward
    '''
    REPAIRS = "Repairs"
    '''
    Vessel is undergoing repairs or Drydock.
    '''
    WAITING_TO_LOAD = "Waiting to Load"
    '''
    Vessel is waiting to load
    '''
    LOADING = "Loading"
    '''
    Vessel is loading, i.e. it has entered a Jetty or is performing STS
    '''
    LADEN = "Laden"
    '''
    Vesel has loaded
    '''
    WAITING_TO_DISCHARGE = "Waiting to Discharge"
    '''
    Vessel is waiting to Discharge
    '''
    DISCHARGING = "Discharging"
    '''
    Vessel is discharging, i.e. it has entered a Jetty or is performing STS
    '''
    ACTIVE_STORAGE = "Active Storage"
    '''
    Vessel is in active storage.
    This means it acts as storage for a
    short term (compared to storage vessels).
    '''
    BALLAST_UNFIXED = "Ballast Unfixed"
    '''
    Vessel is currently free of cargo and not fixed (prompt)
    '''
    BALLAST_FIXED_IMPLIED = "Ballast Fixed (implied)"
    '''
    Vessel is currently free of cargo and her AIS destination implies a fixture
    '''
