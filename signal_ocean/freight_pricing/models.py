# noqa: D100

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class FreightPricing:
    """Freight pricing for a specific vessel class.

    Attributes:
        vessel_class: The vessel class the pricing applies to.
        cargo_quantity: Cargo quantity for the selected load and discharge
            ports.
        rate: Cost of freight in dollars per ton.
        total_freight: Total cost of transporting the given quantity.
    """

    vessel_class: str
    cargo_quantity: Decimal
    rate: Decimal
    total_freight: Decimal
