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
        ([Area('country', LocationTaxonomy.COUNTRY)], 'country'),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('narrow', LocationTaxonomy.NARROW_AREA),
                    Area('wide', LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('narrow', LocationTaxonomy.NARROW_AREA),
                    Area('wide', LocationTaxonomy.WIDE_AREA),
                    Area('country', LocationTaxonomy.COUNTRY)
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
        ([Area('narrow', LocationTaxonomy.NARROW_AREA)], 'narrow'),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('country', LocationTaxonomy.COUNTRY),
                    Area('wide', LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('narrow', LocationTaxonomy.NARROW_AREA),
                    Area('wide', LocationTaxonomy.WIDE_AREA),
                    Area('country', LocationTaxonomy.COUNTRY)
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
        ([Area('wide', LocationTaxonomy.WIDE_AREA)], 'wide'),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('country', LocationTaxonomy.COUNTRY),
                    Area('narrow', LocationTaxonomy.NARROW_AREA)
                ],
                None
        ),
        (
                [
                    Area('port', LocationTaxonomy.PORT),
                    Area('narrow', LocationTaxonomy.NARROW_AREA),
                    Area('wide', LocationTaxonomy.WIDE_AREA),
                    Area('country', LocationTaxonomy.COUNTRY)
                ],
                'wide'
        ),
    ]
)
def test_determines_open_wide_area_by_location_taxonomy(areas, expected_area):
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_wide_area == expected_area
