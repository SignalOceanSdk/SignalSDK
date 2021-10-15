from datetime import date, timedelta
from typing import List

import pytest  # type: ignore

from signal_ocean.tonnage_list import DateRange

a_date = date.today()


def are_equal(left: DateRange, right: DateRange) -> bool:
    return left.start == right.start and left.end == right.end


def test_start_date_cannot_be_after_end_date() -> None:
    with pytest.raises(ValueError) as exception_info:
        DateRange(date.max, a_date)

    assert str(exception_info.value) == "Start date cannot be after end date."


@pytest.mark.parametrize("max_days", [0, -1])  # type: ignore
def test_throws_if_attempted_to_split_into_chunks_smaller_than_a_day(
    max_days: int,
) -> None:
    date_range = DateRange(a_date, a_date)

    with pytest.raises(ValueError) as exception_info:
        list(date_range._split(max_days))

    assert (
        str(exception_info.value)
        == f"Date range cannot be split into chunks of {max_days} days."
    )


@pytest.mark.parametrize(  # type: ignore
    "date_range",
    [DateRange(None, None), DateRange(a_date, None), DateRange(None, a_date)],
)
def test_does_not_split_if_any_of_the_dates_is_optional(
    date_range: DateRange,
) -> None:
    split = list(date_range._split(max_days=1))

    assert len(split) == 1
    assert are_equal(split[0], date_range)


def test_does_not_split_if_date_range_spans_less_than_split_size() -> None:
    date_range = DateRange(a_date, a_date + timedelta(days=1))

    split = list(date_range._split(max_days=2))

    assert len(split) == 1
    assert are_equal(split[0], date_range)


@pytest.mark.parametrize(  # type: ignore
    "date_range, max_days, expected_split",
    [
        (
            # exact split
            DateRange(date(2021, 2, 25), date(2021, 2, 28)),
            2,
            [
                DateRange(date(2021, 2, 25), date(2021, 2, 26)),
                DateRange(date(2021, 2, 27), date(2021, 2, 28)),
            ],
        ),
        (
            # non-exact split
            DateRange(date(2021, 2, 25), date(2021, 2, 27)),
            2,
            [
                DateRange(date(2021, 2, 25), date(2021, 2, 26)),
                DateRange(date(2021, 2, 27), date(2021, 2, 27)),
            ],
        ),
        (
            # split into individual days
            DateRange(date(2021, 2, 25), date(2021, 2, 27)),
            1,
            [
                DateRange(date(2021, 2, 25), date(2021, 2, 25)),
                DateRange(date(2021, 2, 26), date(2021, 2, 26)),
                DateRange(date(2021, 2, 27), date(2021, 2, 27)),
            ],
        ),
    ],
)
def test_splits_into_adjacent_date_ranges(
    date_range: DateRange, max_days: int, expected_split: List[DateRange]
) -> None:
    split = list(date_range._split(max_days))

    assert len(split) == len(expected_split)
    for actual_range, expected_range in zip(split, expected_split):
        assert are_equal(actual_range, expected_range)
