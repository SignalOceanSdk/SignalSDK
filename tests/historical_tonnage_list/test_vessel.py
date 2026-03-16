import pytest

from signal_ocean.historical_tonnage_list import Area, LocationTaxonomy
from .create_vessel import create_vessel


def test_initializes_open_areas_to_empty_tuple_if_None():
    vessel = create_vessel(open_areas=None)

    assert vessel.open_areas == ()


@pytest.mark.parametrize(
    'areas, expected_country',
    [
        ([], None),
        ([Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY)], 'country'),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA),
                    Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA),
                    Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA),
                    Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY)
                ],
                'country'
        ),
    ]
)
def test_determines_open_country_by_location_taxonomy(areas, expected_country):
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_country == expected_country


@pytest.mark.parametrize(
    'areas, expected_area',
    [
        ([], None),
        ([Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA)], 'narrow'),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY),
                    Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA),
                    Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA),
                    Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY)
                ],
                'narrow'
        ),
    ]
)
def test_determines_open_narrow_area_by_location_taxonomy(areas, expected_area):
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_narrow_area == expected_area


@pytest.mark.parametrize(
    'areas, expected_area',
    [
        ([], None),
        ([Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA)], 'wide'),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY),
                    Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA)
                ],
                None
        ),
        (
                [
                    Area(name='port', location_taxonomy=LocationTaxonomy.PORT),
                    Area(name='narrow', location_taxonomy=LocationTaxonomy.NARROW_AREA),
                    Area(name='wide', location_taxonomy=LocationTaxonomy.WIDE_AREA),
                    Area(name='country', location_taxonomy=LocationTaxonomy.COUNTRY)
                ],
                'wide'
        ),
    ]
)
def test_determines_open_wide_area_by_location_taxonomy(areas, expected_area):
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_wide_area == expected_area
