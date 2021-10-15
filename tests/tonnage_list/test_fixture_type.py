from signal_ocean.tonnage_list import FixtureType


def test_can_list_all_fixture_types() -> None:
    fixture_types = list(FixtureType)

    assert fixture_types == ["Scraped", "Manual", "Implied"]
