# noqa: D100

from .._internals import IterableConstants


class LocationTaxonomy(metaclass=IterableConstants):
    """Contains constants for available location taxonomies."""
    PORT = 'Port'
    COUNTRY = 'Country'
    NARROW_AREA = 'Narrow Area'
    WIDE_AREA = 'Wide Area'
