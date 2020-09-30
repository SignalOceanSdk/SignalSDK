from decimal import Decimal
from typing import cast, Mapping, Any

from .._internals import as_decimal
from .models import Country, Port, Area


def parse_country(json: Mapping[str, Any]) -> Country:
    return Country(
        cast(int, json.get("id")),
        cast(str, json.get("name")),
        cast(str, json.get("countryCode")),
        cast(str, json.get("countryCodeNumeric")),
        cast(str, json.get("countryCodeISO3")),
    )


def parse_port(json: Mapping[str, Any]) -> Port:
    return Port(
        cast(int, json.get("id")),
        cast(int, json.get("countryId")),
        cast(int, json.get("areaId")),
        cast(str, json.get("name")),
        cast(Decimal, as_decimal(cast(float, json.get("latitude")))),
        cast(Decimal, as_decimal(cast(float, json.get("longitude")))),
    )


def parse_area(json: Mapping[str, Any]) -> Area:
    return Area(
        cast(int, json.get("id")),
        cast(str, json.get("name")),
        cast(int, json.get("areaTypeId")),
        json.get("parentAreaId"),
    )
