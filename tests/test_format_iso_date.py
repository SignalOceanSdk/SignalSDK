from datetime import date

import pytest

from signal_ocean._internals import format_iso_date

def test_handles_None():
    assert format_iso_date(None) is None

@pytest.mark.parametrize('input_date, expected', [
    (date(2020, 12, 1), '2020-12-01'),
    (date(2020, 1, 10), '2020-01-10'),
    (date(2020, 12, 31), '2020-12-31')
])
def test_returns_date_string_in_ISO_format(input_date: date, expected: str):
    assert format_iso_date(input_date) == expected