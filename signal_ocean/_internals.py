from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Union, Optional

from dateutil import parser


class IterableConstants(type):
    def __iter__(cls):
        return (
            value for (key, value) in cls.__dict__.items()
            if not key.startswith('_') and key.isupper()
        )


def contains_caseless(pattern: str, target: str) -> bool:
    return bool(
        pattern is not None
        and target is not None
        and pattern.casefold() in target.casefold()
    )


def format_iso_date(value: date) -> str:
    return value.strftime('%Y-%m-%d') if value else None


def as_decimal(value: Union[float, str]) -> Optional[Decimal]:
    return Decimal(str(value)) if value else None


def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        result = parser.isoparse(value)
    except (TypeError, ValueError):
        return None

    return result.replace(tzinfo=timezone.utc)
