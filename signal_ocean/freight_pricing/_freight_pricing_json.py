from typing import Iterable, Tuple, cast, Mapping, Any
from decimal import Decimal

from .models import FreightPricing
from .._internals import as_decimal


def parse(json: Iterable[Mapping[str, Any]]) -> Tuple[FreightPricing, ...]:
    return tuple(parse_freight_pricing_item(i) for i in json)


def parse_freight_pricing_item(json: Mapping[str, Any]) -> FreightPricing:
    return FreightPricing(
        cast(str, json.get("vesselClass")),
        cast(Decimal, as_decimal(cast(float, json.get("cargoQuantity")))),
        cast(Decimal, as_decimal(cast(float, json.get("rate")))),
        cast(Decimal, as_decimal(cast(float, json.get("totalFreight")))),
    )
