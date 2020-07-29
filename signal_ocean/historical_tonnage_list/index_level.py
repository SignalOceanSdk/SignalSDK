# noqa: D100

from .._internals import IterableConstants


class IndexLevel(metaclass=IterableConstants):
    """Contains constants for available data frame index levels."""
    DATE = 'date'
    IMO = 'imo'
