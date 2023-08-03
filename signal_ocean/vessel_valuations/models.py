# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List


@dataclass(frozen=True)
class Valuation:
    """A valuation for a specific vessel.

    Attributes:
        imo: The IMO number of the vessel the valuation applies to.
        valuation_price: The price of the valuation.
        scrap_price: The estimated scrapped valuation of the vessel.
        updated_date: Date and time at which the valuation was updated.
    """
    imo: Optional[int] = 0
    valuation_price: Optional[Decimal] = 0
    scrap_price: Optional[Decimal] = 0
    updated_date: Optional[str] = None


class HistoricalValuation(frozen=True):
    """A historical valuation for a specific vessel.

    Attributes:
        imo: The IMO number of the vessel the valuation applies to.
        value_from: Date and time at which the valuation was updated.
        valuation_price: The price of the valuation.
        scrap_price: The estimated scrapped valuation of the vessel.

    """
    imo: Optional[int] = 0
    value_from: Optional[str] = None
    valuation_price: Optional[Decimal] = 0
    scrap_price: Optional[Decimal] = 0


class PageValuations(frozen=True):
    """The estimated valuations by page.

    Attributes:
        page:  The page number you are requesting.
        page_size:  The maximum number of results per
        page to be returned. Range between 1 and 500, by default 100.
        total: The total number of available results.
        valuations: A list/array that contains the results of the requested vessel valuations.
    """

    page: Optional[int] = 1
    page_size: Optional[int] = 100
    total: Optional[int] = 20820
    valuations: Optional[List[Valuation]] = None



