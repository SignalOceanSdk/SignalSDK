# noqa: D100

from .._internals import IterableConstants


class PushType(metaclass=IterableConstants):
    """Contains constants for available push types."""
    NOT_PUSHED = 'Not Pushed'
    PUSHED_POSS = 'Pushed POSS'
    PUSHED = 'Pushed'
