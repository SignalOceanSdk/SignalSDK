from datetime import datetime
from typing import Iterable, Tuple, cast, Dict, Any

from .models import Valuation
from .._internals import parse_datetime, as_decimal


def parse_valuations(json: Iterable[Dict[str, Any]]) -> Tuple[Valuation, ...]:
    return tuple(parse_valuation(s) for s in json)


def parse_valuation(json: Dict[str, Any]) -> Valuation:
    return Valuation(
        cast(int, json.get("imo")),
        cast(datetime, parse_datetime(json.get("valueFrom"))),
        as_decimal(json.get("valuationPrice")),
        cast(datetime, parse_datetime(json.get("updatedDate"))),
    )
