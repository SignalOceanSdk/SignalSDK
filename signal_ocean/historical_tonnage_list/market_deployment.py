# noqa: D100

from .._internals import IterableConstants


class MarketDeployment(metaclass=IterableConstants):
    """Contains constants for available market deployments."""
    SPOT = 'Spot'
    PROGRAM = 'Program'
    RELET = 'Relet'
    CONTRACT = 'Contract'
