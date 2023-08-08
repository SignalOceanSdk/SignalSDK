# noqa: D100
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


def _to_camel_case_custom(s: str,
                          rename_keys: Optional[Dict[str, str]] = None) -> str:
    """Transforms a string from snake_case to camel_case.

    Args:
        s: The string to transform
        rename_keys: Key names to transform explicitly to the desired
            target string when the default output is not adequate.

    Returns:
        The transformed string
    """
    _to_camelcase = s.split('_')
    _to_camelcase = [
        word.capitalize() if _to_camelcase.index(word) > 0
        else word for word in _to_camelcase
    ]
    result = ''.join(_to_camelcase)

    if rename_keys:
        if s in rename_keys:
            result = rename_keys[s]

    return result


@dataclass(frozen=True)
class Valuation:
    """A valuation for a specific vessel.

    Attributes:
        imo: The IMO number of the vessel the valuation applies to.
        valuation_price: The price of the valuation.
        scrap_price: The estimated scrapped valuation of the vessel.
        updated_date: Date and time at which the valuation was updated.
    """
    imo: int
    valuation_price: float
    scrap_price: float
    updated_date: str

    def to_dict(self) -> Dict[Any, Any]:
        """Cast Valuation object to dict.

        Returns:
            Dict representation of Valuation model

        """
        return asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case_custom(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class HistoricalValuation:
    """A historical valuation for a specific vessel.

    Attributes:
        imo: The IMO number of the vessel the valuation applies to.
        value_from: Date and time at which the valuation was updated.
        valuation_price: The price of the valuation.
        scrap_price: The estimated scrapped valuation of the vessel.
    """
    imo: int
    value_from: str
    valuation_price: float
    scrap_price: float

    def to_dict(self) -> Dict[Any, Any]:
        """Cast HistoricalValuation object to dict.

        Returns:
            Dict representation of HistoricalValuation model

        """
        return asdict(
            self,
            dict_factory=lambda x: {
                _to_camel_case_custom(k): v
                for (k, v) in x if v is not None
            })


@dataclass(frozen=True)
class PageValuations:
    """The estimated valuations by page.

    Attributes:
        page:  The page number you are requesting.
        page_size:  The maximum number of results per
        page to be returned. Range between 1 and 500, by default 100.
        total: The total number of available results.
        valuations: A list/array that contains
        the results of the requested vessel valuations.
    """

    page: int
    page_size: int
    total: Optional[int]
    valuations: List[Valuation]

    def to_dict(self) -> Dict[Any, Any]:
        """Cast PageValuations object to dict.

        Returns:
            Dict representation of PageValuations object

        """
        return {
            "page": self.page,
            "pageSize": self.page_size,
            "total": self.total,
            "valuations": [valuation.to_dict()
                           for valuation in self.valuations]
        }
