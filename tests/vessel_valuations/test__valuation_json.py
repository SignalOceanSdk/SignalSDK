from datetime import datetime, timezone
from decimal import Decimal

from signal_ocean.vessel_valuations import ValuationSummary, ValuationHistory
from signal_ocean.vessel_valuations._valuation_json import parse_summary, parse_valuation_history


def test_handles_missing_values():
    summary = parse_summary({})

    assert summary == ValuationSummary(None, None, None, None)


def test_parses_valuation_summary():
    summary = parse_summary({
        'imo': 1234567,
        'valueFrom': '2020-05-15T00:00:00',
        'valuationPrice': 1.2345,
        'updatedDate': '2020-05-19T17:41:10.64'
    })

    assert summary == ValuationSummary(
        1234567,
        datetime(2020, 5, 15, tzinfo=timezone.utc),
        Decimal('1.2345'),
        datetime(2020, 5, 19, 17, 41, 10, 640000, timezone.utc)
    )


def test_parses_valuation_history():
    summaries = parse_valuation_history([
        {
            'imo': 1234567,
            'valueFrom': '2020-05-15T00:00:00',
            'valuationPrice': 1.2345,
            'updatedDate': '2020-05-19T17:41:10.64'
        },
        {
            'imo': 7654321,
            'valueFrom': '2020-06-15T00:00:00',
            'valuationPrice': 2.3456,
            'updatedDate': '2020-06-19T17:00:00'
        }
    ])

    assert len(summaries) == 2
    assert summaries[0] == ValuationSummary(
        1234567,
        datetime(2020, 5, 15, tzinfo=timezone.utc),
        Decimal('1.2345'),
        datetime(2020, 5, 19, 17, 41, 10, 640000, timezone.utc)
    )
    assert summaries[1] == ValuationSummary(
        7654321,
        datetime(2020, 6, 15, tzinfo=timezone.utc),
        Decimal('2.3456'),
        datetime(2020, 6, 19, 17, tzinfo=timezone.utc)
    )
