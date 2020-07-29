from typing import List
from decimal import Decimal

from .freight_pricing import FreightPricing, FreightPricingItem
from .._internals import as_decimal


def parse(json: List[dict]) -> FreightPricing:
    return FreightPricing(
        parse_freight_pricing_item(i) for i in json
    )


def parse_freight_pricing_item(json: dict) -> FreightPricingItem:
    return FreightPricingItem(
        json.get('vesselClass'),
        as_decimal(json.get('cargoQuantity')),
        as_decimal(json.get('rate')),
        as_decimal(json.get('totalFreight'))
    )

