import pytest

from signal_ocean import PortFilter
from .builders import create_port


def test_does_not_filter_anything_by_default():
    port_filter = PortFilter()
    unfiltered = [create_port(1), create_port(2)]

    filtered = port_filter._apply(unfiltered)

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
def test_filters_ports_by_name(name_like: str):
    port_filter = PortFilter(name_like=name_like)
    unmatched = create_port(1, 'x')
    matched = create_port(3, 'matching name')

    filtered = port_filter._apply([unmatched, matched])

    assert list(filtered) == [matched]
