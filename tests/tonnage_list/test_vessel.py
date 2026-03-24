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
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=0),
            ),
             "country",
        ),
        (
            (
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=1),
                Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=2),
                Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=3),
            ),
            None,
        ),
        (
            (
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=0),
                Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=1),
                Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=2),
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=3),
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
        ((Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=0),), "narrow"),
        (
            (
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=0),
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=0),
                Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=0),
            ),
            None,
        ),
        (
            (
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=0),
                Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=0),
                Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=0),
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=0),
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
        ([Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=0)], "wide"),
        (
            [
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=0),
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=0),
                Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=0),
            ],
            None,
        ),
        (
            [
                Area(id=123, name="port", location_taxonomy=LocationTaxonomy.PORT, taxonomy_id=0),
                Area(id=123, name="narrow", location_taxonomy=LocationTaxonomy.NARROW_AREA, taxonomy_id=0),
                Area(id=123, name="wide", location_taxonomy=LocationTaxonomy.WIDE_AREA, taxonomy_id=0),
                Area(id=123, name="country", location_taxonomy=LocationTaxonomy.COUNTRY, taxonomy_id=0),
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
