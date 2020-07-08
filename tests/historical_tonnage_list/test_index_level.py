from signal_ocean.historical_tonnage_list import IndexLevel


def test_can_list_all_index_level_names():
    levels = list(IndexLevel)

    assert levels == ['date', 'imo']
