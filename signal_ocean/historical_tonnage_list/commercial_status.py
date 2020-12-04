# noqa: D100

from .._internals import IterableConstants


class CommercialStatus(metaclass=IterableConstants):
    """Contains constants for available commercial statuses."""
    ON_SUBS = 'On Subs'
    """
    Vessel is On Subs for a new Fixture.
    """
    FAILED = 'Failed'
    """
    Last fixture failed for this Vessel.
    """
    CANCELLED = 'Cancelled'
    """
    Last fixture cancelled for this Vessel.
    """
    AVAILABLE = 'Available'
    """
    Vessel is available for a new voyage after her open date.
    """
    POTENTIALLY_FIXED = 'Poss Fixed'
    """
    Systems assumes the vessel is fixed for her new voyage based
        on AIS information
    """
