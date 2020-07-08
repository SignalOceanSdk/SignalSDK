from signal_ocean.historical_tonnage_list import LocationTaxonomy


def test_can_list_available_taxonomies():
    taxonomies = list(LocationTaxonomy)

    assert taxonomies == ['Port', 'Country', 'Narrow Area', 'Wide Area']
