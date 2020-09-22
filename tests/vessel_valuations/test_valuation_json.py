from datetime import datetime, timezone
from decimal import Decimal

from signal_ocean.vessel_valuations import Valuation
from signal_ocean.vessel_valuations._valuation_json import (
    parse_valuation,
    parse_valuations,
)


def test_handles_missing_values():
    valuation = parse_valuation({})

    assert valuation == Valuation(None, None, None, None)


def test_parses_valuation():
    valuation = parse_valuation(
        {
            "imo": 1234567,
            "valueFrom": "2020-05-15T00:00:00",
            "valuationPrice": 1.2345,
            "updatedDate": "2020-05-19T17:41:10.64",
        }
    )

    assert valuation == Valuation(
        1234567,
        datetime(2020, 5, 15, tzinfo=timezone.utc),
        Decimal("1.2345"),
        datetime(2020, 5, 19, 17, 41, 10, 640000, timezone.utc),
    )


def test_parses_valuations():
    valuations = parse_valuations(
        [
            {
                "imo": 1234567,
                "valueFrom": "2020-05-15T00:00:00",
                "valuationPrice": 1.2345,
                "updatedDate": "2020-05-19T17:41:10.64",
            },
            {
                "imo": 7654321,
                "valueFrom": "2020-06-15T00:00:00",
                "valuationPrice": 2.3456,
                "updatedDate": "2020-06-19T17:00:00",
            },
        ]
    )

    assert len(valuations) == 2
    assert valuations[0] == Valuation(
        1234567,
        datetime(2020, 5, 15, tzinfo=timezone.utc),
        Decimal("1.2345"),
        datetime(2020, 5, 19, 17, 41, 10, 640000, timezone.utc),
    )
    assert valuations[1] == Valuation(
        7654321,
        datetime(2020, 6, 15, tzinfo=timezone.utc),
        Decimal("2.3456"),
        datetime(2020, 6, 19, 17, tzinfo=timezone.utc),
    )
