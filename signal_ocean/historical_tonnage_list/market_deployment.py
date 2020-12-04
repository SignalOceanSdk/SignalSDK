# noqa: D100

from .._internals import IterableConstants


class MarketDeployment(metaclass=IterableConstants):
    """Contains constants for available market deployments."""
    SPOT = 'Spot'
    '''
    Vessels controlled by commercial operators that participate in the
    spot market and are advertised through Tonnage lists and
    get reported fixtures
    '''
    PROGRAM = 'Program'
    '''
    Vessels controlled by charterers like
    that do not participate in the spot market and
    are either not advertised through Tonnage lists or
    Tonnage lists report the fact that they are program
    '''
    RELET = 'Relet'
    '''
    Vessels controlled by charterers that participate in the spot market
    and are advertised through Tonnage lists and get reported fixtures
    '''
    CONTRACT = 'Contract'
    '''
    Vessels controlled by commercial operators that do not participate
    in the spot market and are typically
    doing system cargoes with repetitive trading patterns.
    '''
