# noqa: D100

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Sequence


@dataclass(frozen=True)
class FreightPricingItem:
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


class FreightPricing(Sequence):
    """Contains freight prices to move commodities between two ports."""

    def __init__(self, items: Iterable[FreightPricingItem]):
        """Initializes freight pricing.
        
        Args:
            items: Items to be contained within this freight pricing.
        """
        self.__items = tuple(items)

    def __getitem__(self, index) -> FreightPricingItem: # noqa: D105
        return self.__items.__getitem__(index)

    def __len__(self) -> int:   # noqa: D105
        return self.__items.__len__()

    def __repr__(self) -> str:  # noqa: D105
        return repr(self.__items)
