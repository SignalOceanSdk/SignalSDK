from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Union, Optional, Mapping, Iterable, Iterator

from dateutil import parser

QueryStringParam = Union[str, int, float, Iterable[Union[str, int, float]]]
QueryString = Mapping[str, Optional[QueryStringParam]]


class IterableConstants(type):
    def __iter__(cls) -> Iterator[str]:
        return (
            value
            for (key, value) in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        )


def contains_caseless(pattern: str, target: str) -> bool:
    return bool(
        pattern is not None
        and target is not None
        and pattern.casefold() in target.casefold()
    )


def format_iso_date(value: Optional[date]) -> Optional[str]:
    return value.strftime("%Y-%m-%d") if value else None


def format_iso_datetime(value: Optional[datetime]) -> Optional[str]:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ") if value else None


def as_decimal(value: Optional[Union[float, str]]) -> Optional[Decimal]:
    try:
        return Decimal(str(value)) if value is not None else None
    except (InvalidOperation):
        return None


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        result = parser.isoparse(value)
    except (TypeError, ValueError):
        return None

    return result.replace(tzinfo=timezone.utc)


def snake_to_camel_case(input_string: str) -> str:
    """Function to reformat input string from snake_case to CamelCase.

    Args:
        input_string: The inpyt string.

    Returns:
        Input string converted to CamelCase.
    """
    temp = input_string.split('_')
    for i, s in enumerate(temp):
        temp[i] = s[0].upper() + s[1:]
        result = temp[0] + ''.join(x.title() for x in temp[1:])
    return result
