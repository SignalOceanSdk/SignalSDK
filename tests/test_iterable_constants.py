from signal_ocean._internals import IterableConstants


def test_lists_class_object_attribute_values():
    class Constants(metaclass=IterableConstants):
        C1 = 'A'
        C2 = 'B'

    values = list(Constants)

    assert values == ['A', 'B']


def test_does_not_list_sunders_and_dunders():
    class Constants(metaclass=IterableConstants):
        _sunder = 'sunder'
        __dunder = 'dunder'

    values = list(Constants)

    assert values == []
