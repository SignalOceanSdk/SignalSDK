from datetime import date, timedelta
from typing import List

import pytest

from signal_ocean.historical_tonnage_list.historical_tonnage_list_api import (
    _DateRange,
)

a_date = date.today()


def are_equal(left: _DateRange, right: _DateRange) -> bool:
    return left.start == right.start and left.end == right.end


def test_start_date_cannot_be_after_end_date():
    with pytest.raises(ValueError) as exception_info:
        _DateRange(date.max, a_date)

    assert str(exception_info.value) == "Start date cannot be after end date."


@pytest.mark.parametrize("max_days", [0, -1])
def test_throws_if_attempted_to_split_into_chunks_smaller_than_a_day(
    max_days: int,
):
    date_range = _DateRange(a_date, a_date)

    with pytest.raises(ValueError) as exception_info:
        list(date_range.split(max_days))

    assert (
        str(exception_info.value)
        == f"Date range cannot be split into chunks of {max_days} days."
    )


@pytest.mark.parametrize(
    "date_range",
    [_DateRange(None, None), _DateRange(a_date, None), _DateRange(None, a_date)],
)
def test_does_not_split_if_any_of_the_dates_is_optional(date_range: _DateRange):
    split = list(date_range.split(max_days=1))

    assert len(split) == 1
    assert are_equal(split[0], date_range)


def test_does_not_split_if_date_range_spans_less_than_split_size():
    date_range = _DateRange(a_date, a_date + timedelta(days=1))

    split = list(date_range.split(max_days=2))

    assert len(split) == 1
    assert are_equal(split[0], date_range)


@pytest.mark.parametrize(
    "date_range, max_days, expected_split",
    [
        (
            # exact split
            _DateRange(date(2021, 2, 25), date(2021, 2, 28)),
            2,
            [
                _DateRange(date(2021, 2, 25), date(2021, 2, 26)),
                _DateRange(date(2021, 2, 27), date(2021, 2, 28)),
            ],
        ),
        (
            # non-exact split
            _DateRange(date(2021, 2, 25), date(2021, 2, 27)),
            2,
            [
                _DateRange(date(2021, 2, 25), date(2021, 2, 26)),
                _DateRange(date(2021, 2, 27), date(2021, 2, 27)),
            ],
        ),
        (
            # split into individual days
            _DateRange(date(2021, 2, 25), date(2021, 2, 27)),
            1,
            [
                _DateRange(date(2021, 2, 25), date(2021, 2, 25)),
                _DateRange(date(2021, 2, 26), date(2021, 2, 26)),
                _DateRange(date(2021, 2, 27), date(2021, 2, 27)),
            ],
        ),
    ],
)
def test_splits_into_adjacent_date_ranges(
    date_range: _DateRange, max_days: int, expected_split: List[_DateRange]
):
    split = list(date_range.split(max_days))

    assert len(split) == len(expected_split)
    for actual_range, expected_range in zip(split, expected_split):
        assert are_equal(actual_range, expected_range)
