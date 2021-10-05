from signal_ocean.tonnage_list import IndexLevel


def test_can_list_all_index_level_names() -> None:
    levels = list(IndexLevel)

    assert levels == ["date", "imo"]
