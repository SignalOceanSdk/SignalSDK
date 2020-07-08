from .._internals import IterableConstants


class PushType(metaclass=IterableConstants):
    NOT_PUSHED = 'Not Pushed'
    PUSHED_POSS = 'Pushed POSS'
    PUSHED = 'Pushed'
