from typing import List, Tuple
import pytest  # type: ignore

from signal_ocean.tonnage_list import Area, LocationTaxonomy
from .builders import create_vessel


def test_initializes_open_areas_to_empty_tuple_if_None() -> None:
    vessel = create_vessel(open_areas=None)  # type: ignore

    assert vessel.open_areas == ()


@pytest.mark.parametrize(  # type: ignore
    "areas, expected_country",
    [
        (
            (), 
            None,
        ),
        (
            (
                Area(123,"country", LocationTaxonomy.COUNTRY,0),
            ),
             "country",
        ),
        (
            (
                Area(123,"port", LocationTaxonomy.PORT,1),
                Area(123,"narrow", LocationTaxonomy.NARROW_AREA,2),
                Area(123,"wide", LocationTaxonomy.WIDE_AREA,3),
            ),
            None,
        ),
        (
            (
                Area(123,"port", LocationTaxonomy.PORT,0),
                Area(123,"narrow", LocationTaxonomy.NARROW_AREA,1),
                Area(123,"wide", LocationTaxonomy.WIDE_AREA,2),
                Area(123,"country", LocationTaxonomy.COUNTRY,3),
            ),
            "country",
        ),
    ],
)
def test_determines_open_country_by_location_taxonomy(
    areas: Tuple[Area,...], expected_country: str
) -> None:
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_country == expected_country


@pytest.mark.parametrize(  # type: ignore
    "areas, expected_area",
    [
        ((), None),
        ((Area(123,"narrow", LocationTaxonomy.NARROW_AREA,0),), "narrow"),
        (
            (
                Area(123,"port", LocationTaxonomy.PORT,0),
                Area(123,"country", LocationTaxonomy.COUNTRY,0),
                Area(123,"wide", LocationTaxonomy.WIDE_AREA,0),
            ),
            None,
        ),
        (
            (
                Area(123,"port", LocationTaxonomy.PORT,0),
                Area(123,"narrow", LocationTaxonomy.NARROW_AREA,0),
                Area(123,"wide", LocationTaxonomy.WIDE_AREA,0),
                Area(123,"country", LocationTaxonomy.COUNTRY,0),
            ),
            "narrow",
        ),
    ],
)
def test_determines_open_narrow_area_by_location_taxonomy(
    areas: Tuple[Area,...], expected_area: str
) -> None:
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_narrow_area == expected_area


@pytest.mark.parametrize(  # type: ignore
    "areas, expected_area",
    [
        ([], None),
        ([Area(123,"wide", LocationTaxonomy.WIDE_AREA,0)], "wide"),
        (
            [
                Area(123,"port", LocationTaxonomy.PORT,0),
                Area(123,"country", LocationTaxonomy.COUNTRY,0),
                Area(123,"narrow", LocationTaxonomy.NARROW_AREA,0),
            ],
            None,
        ),
        (
            [
                Area(123,"port", LocationTaxonomy.PORT,0),
                Area(123,"narrow", LocationTaxonomy.NARROW_AREA,0),
                Area(123,"wide", LocationTaxonomy.WIDE_AREA,0),
                Area(123,"country", LocationTaxonomy.COUNTRY,0),
            ],
            "wide",
        ),
    ],
)
def test_determines_open_wide_area_by_location_taxonomy(
    areas: Tuple[Area,...], expected_area: str
) -> None:
    vessel = create_vessel(open_areas=areas)

    assert vessel.open_wide_area == expected_area
