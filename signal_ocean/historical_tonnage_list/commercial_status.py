# noqa: D100

from .._internals import IterableConstants


class CommercialStatus(metaclass=IterableConstants):
    """Contains constants for available commercial statuses."""
    ON_SUBS = 'On Subs'
    FAILED = 'Failed'
    CANCELLED = 'Cancelled'
    AVAILABLE = 'Available'
    POTENTIALLY_FIXED = 'Potentially Fixed'
