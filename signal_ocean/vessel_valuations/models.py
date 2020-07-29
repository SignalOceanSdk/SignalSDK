# noqa: D100

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Sequence, Iterable, Optional


@dataclass(frozen=True)
class ValuationSummary:
    """A valuation summary.

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


class ValuationHistory(Sequence):
    """An immutable collection of valuation summaries."""

    def __init__(self, summaries: Iterable[ValuationSummary]):
        """Initializes ValuationHistory.

        Args:
            summaries: A collection of summaries.
        """
        self.__summaries = tuple(summaries)

    def __getitem__(self, index) -> ValuationSummary:   # noqa: D105
        return self.__summaries.__getitem__(index)

    def __len__(self) -> int:   # noqa: D105
        return self.__summaries.__len__()

    def __repr__(self) -> str:  # noqa: D105
        return repr(self.__summaries)
