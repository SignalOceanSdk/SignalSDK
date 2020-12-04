# noqa: D100
# pylint: disable=W0105

from .._internals import IterableConstants


class LocationTaxonomy(metaclass=IterableConstants):
    """Contains constants for available location taxonomies."""
    PORT = 'Port'
    """
    Location Taxonomy Port.
    """
    COUNTRY = 'Country'
    """
    Location Taxonomy Country.
    """
    NARROW_AREA = 'Narrow Area'
    """
    Location Taxonomy Narrow Area.
    """
    WIDE_AREA = 'Wide Area'
    """
    Location Taxonomy Wide Area.
    """
