from signal_ocean.historical_tonnage_list import FixtureType


def test_can_list_all_fixture_types():
    fixture_types = list(FixtureType)

    assert fixture_types == ['Scraped', 'Manual', 'Implied']
