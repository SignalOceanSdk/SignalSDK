# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Valuation:
    """A valuation for a specific vessel.

    Attributes:
        imo: The IMO number of the vessel the valuation applies to.
        value_from: Date and time at which the valuation occurred.
        valuation_price: The price of the valuation.
        updated_date: Date and time at which the valuation was updated.
    """
    imo: int
    value_from: datetime
    valuation_price: Optional[Decimal]
    updated_date: datetime
