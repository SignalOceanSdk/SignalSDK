# noqa: D100

from .._internals import IterableConstants


class FixtureType(metaclass=IterableConstants):
    """Contains constants for available fixture types."""
    SCRAPED = 'Scraped'
    MANUAL = 'Manual'
    IMPLIED = 'Implied'
