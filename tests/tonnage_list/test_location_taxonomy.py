from signal_ocean.tonnage_list import LocationTaxonomy


def test_can_list_available_taxonomies() -> None:
    taxonomies = list(LocationTaxonomy)

    assert taxonomies == ["Port", "Country", "Narrow Area", "Wide Area"]
