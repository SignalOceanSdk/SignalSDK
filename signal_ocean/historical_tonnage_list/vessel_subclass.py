from .._internals import IterableConstants


class VesselSubclass(metaclass=IterableConstants):
    ALL = None
    DIRTY = 'Dirty'
    CLEAN = 'Clean'
