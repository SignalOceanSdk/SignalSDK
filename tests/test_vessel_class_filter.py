import pytest

from signal_ocean import VesselClassFilter
from .builders import create_vessel_class


def test_does_not_filter_anything_by_default():
    vessel_class_filter = VesselClassFilter()
    unfiltered = [create_vessel_class(1), create_vessel_class(2)]

    filtered = vessel_class_filter._apply(unfiltered)

    assert list(filtered) == unfiltered


@pytest.mark.parametrize(
    'name_like',
    [
        'matching name', 'matching', 'name', 'mat', 'me', 'ing na',
        'MATCHING NAME', 'MATCHING', 'NAME', 'MAT', 'ME', 'ING NA',
        'mAtchiNG NamE', 'Matching', 'nAME', 'MaT', 'mE', 'INg nA',
        ' '
    ]
)
def test_filters_vessel_classes_by_name(name_like: str):
    vessel_class_filter = VesselClassFilter(name_like=name_like)
    unmatched = create_vessel_class(1, 'x')
    matched = create_vessel_class(3, 'matching name')

    filtered = vessel_class_filter._apply([unmatched, matched])

    assert list(filtered) == [matched]
