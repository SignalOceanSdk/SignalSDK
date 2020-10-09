from typing import Iterable, Tuple, cast, Mapping, Any
from decimal import Decimal

from .models import FreightPricing, Costs, Totals
from .._internals import as_decimal

JsonObject = Mapping[str, Any]


def parse(json: Iterable[JsonObject]) -> Tuple[FreightPricing, ...]:
    return tuple(parse_freight_pricing_item(i) for i in json)


def parse_freight_pricing_item(json: JsonObject) -> FreightPricing:
    return FreightPricing(
        cast(str, json.get("vesselClass")),
        cast(Decimal, as_decimal(cast(float, json.get("cargoQuantity")))),
        parse_costs(cast(JsonObject, json.get("costs"))),
        parse_totals(cast(JsonObject, json.get("totals"))),
    )


def parse_costs(json: JsonObject) -> Costs:
    return Costs(
        cast(Decimal, as_decimal(json.get("freightRate"))),
        cast(Decimal, as_decimal(json.get("freightCost"))),
        cast(Decimal, as_decimal(json.get("canal")))
    )


def parse_totals(json: JsonObject) -> Totals:
    return Totals(
        cast(Decimal, as_decimal(json.get("totalCost"))),
        cast(Decimal, as_decimal(json.get("totalCostPerTon"))),
    )
