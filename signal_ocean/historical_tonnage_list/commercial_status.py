from .._internals import IterableConstants


class CommercialStatus(metaclass=IterableConstants):
    ON_SUBS = 'On Subs'
    FAILED = 'Failed'
    CANCELLED = 'Cancelled'
    AVAILABLE = 'Available'
