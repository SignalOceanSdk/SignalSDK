from datetime import datetime, timezone

import pytest

from signal_ocean._internals import parse_datetime


def test_handles_None():
    assert parse_datetime(None) is None


def test_handles_bad_formats():
    assert parse_datetime('not a datetime') is None


@pytest.mark.parametrize(
    'date_string',
    [
        '2020-05-28T00:00:00Z',
        '2020-05-28T00:00:00'
    ])
def test_treats_all_timestamps_as_UTC(date_string: str):
    result = parse_datetime(date_string)

    assert result == datetime(
        year=2020, month=5, day=28, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
