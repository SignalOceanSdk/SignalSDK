from typing import List

from .models import ValuationSummary, ValuationHistory
from .._internals import parse_datetime, as_decimal


def parse_valuation_history(json: List[dict]) -> ValuationHistory:
    return ValuationHistory(
        parse_summary(s) for s in json
    )


def parse_summary(json: dict) -> ValuationSummary:
    return ValuationSummary(
        json.get('imo'),
        parse_datetime(json.get('valueFrom')),
        as_decimal(json.get('valuationPrice')),
        parse_datetime(json.get('updatedDate'))
    )
