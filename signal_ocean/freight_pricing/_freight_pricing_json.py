from typing import Iterable, Tuple, cast, Mapping, Any
from decimal import Decimal

from .models import FreightPricing, Costs, Totals
from .._internals import as_decimal

JsonObject = Mapping[str, Any]


def parse(json: Iterable[JsonObject]) -> Tuple[FreightPricing, ...]:
    return tuple(parse_freight_pricing_item(i) for i in json)


def parse_freight_pricing_item(json: JsonObject) -> FreightPricing:
    return FreightPricing(
        vessel_class=cast(str, json.get("vesselClass")),
        cargo_quantity=cast(Decimal, as_decimal(cast(float, json.get("cargoQuantity")))),
        costs=parse_costs(cast(JsonObject, json.get("costs"))),
        totals=parse_totals(cast(JsonObject, json.get("totals"))),
    )


def parse_costs(json: JsonObject) -> Costs:
    return Costs(
        freight_rate=cast(Decimal, as_decimal(json.get("freightRate"))),
        freight_cost=cast(Decimal, as_decimal(json.get("freightCost"))),
        canal=cast(Decimal, as_decimal(json.get("canal"))),
    )


def parse_totals(json: JsonObject) -> Totals:
    return Totals(
        total_cost=cast(Decimal, as_decimal(json.get("totalCost"))),
        total_cost_per_ton=cast(Decimal, as_decimal(json.get("totalCostPerTon"))),
    )
