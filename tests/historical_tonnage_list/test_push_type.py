from signal_ocean.historical_tonnage_list import PushType


def test_can_list_available_push_types():
    push_types = list(PushType)

    assert push_types == ['Not Pushed', 'Pushed POSS', 'Pushed']
