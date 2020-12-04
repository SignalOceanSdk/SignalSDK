# noqa: D100

from .._internals import IterableConstants


class PushType(metaclass=IterableConstants):
    """Contains constants for available push types."""
    NOT_PUSHED = 'Not Pushed'
    '''
    vessels not pushed anymore
    '''
    PUSHED_POSS = 'Pushed POSS'
    '''
    Actively pushed in the market with notification Poss (Possibly)
    meaning that this is a broker projection
    '''
    PUSHED = 'Pushed'
    '''
    Actively pushed in the market through Tonnage lists or Positions lists
    '''
