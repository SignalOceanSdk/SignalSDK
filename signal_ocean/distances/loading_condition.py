# noqa: D100

from .._internals import IterableConstants


class LoadingCondition(metaclass=IterableConstants):
    """Contains constants for available loading conditions."""
    LADEN = 1
    '''
    Vessel is loaded.
    '''
    BALLAST = 2
    '''
    Vessel is free of cargo
    '''
