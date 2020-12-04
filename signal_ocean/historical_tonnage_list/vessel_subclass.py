# noqa: D100

from .._internals import IterableConstants


class VesselSubclass(metaclass=IterableConstants):
    """Contains constants for available vessel subclasses."""

    ALL = None
    '''
    Refers to all the vessels without any classification regarding
    the cargo type that they are carrying.
    '''
    DIRTY = 'Dirty'
    '''
    Refers to all the vessels that they classify
        to the dirty types of oil cargo.
    Applicable only for Tankers.
    '''
    CLEAN = 'Clean'
    '''
    Refers to all the vessels that they classify
        to the clean types of oil cargo.
    Applicable only for Tankers.
    '''
