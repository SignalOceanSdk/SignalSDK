import pytest

from signal_ocean.historical_tonnage_list import OpenArea, LocationTaxonomy
from .create_vessel import create_vessel


def test_initializes_open_areas_to_empty_tuple_if_None():
    vessel = create_vessel(open_areas=None)

    assert vessel.open_areas == ()


@pytest.mark.parametrize(
    'areas, expected_country',
    [
        ([], None),
        ([OpenArea('country', LocationTaxonomy.COUNTRY)], 'country'),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('narrow', LocationTaxonomy.NARROW_AREA),
                    OpenArea('wide', LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('narrow', LocationTaxonomy.NARROW_AREA),
                    OpenArea('wide', LocationTaxonomy.WIDE_AREA),
                    OpenArea('country', LocationTaxonomy.COUNTRY)
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
        ([OpenArea('narrow', LocationTaxonomy.NARROW_AREA)], 'narrow'),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('country', LocationTaxonomy.COUNTRY),
                    OpenArea('wide', LocationTaxonomy.WIDE_AREA)
                ],
                None
        ),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('narrow', LocationTaxonomy.NARROW_AREA),
                    OpenArea('wide', LocationTaxonomy.WIDE_AREA),
                    OpenArea('country', LocationTaxonomy.COUNTRY)
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
        ([OpenArea('wide', LocationTaxonomy.WIDE_AREA)], 'wide'),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('country', LocationTaxonomy.COUNTRY),
                    OpenArea('narrow', LocationTaxonomy.NARROW_AREA)
                ],
                None
        ),
        (
                [
                    OpenArea('port', LocationTaxonomy.PORT),
                    OpenArea('narrow', LocationTaxonomy.NARROW_AREA),
                    OpenArea('wide', LocationTaxonomy.WIDE_AREA),
                    OpenArea('country', LocationTaxonomy.COUNTRY)
                ],
                'wide'
        ),
    ]
)
def test_determines_open_wide_area_by_location_taxonomy(areas, expected_area):
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_wide_area == expected_area
