# noqa: D100

from decimal import Decimal
from typing import Optional, Callable, TypeVar, Tuple

import requests

from .models import Valuation
from . import _valuation_json
from ..connection import Connection
from .._internals import as_decimal

TValuation = TypeVar("TValuation")


class VesselValuationsAPI:
    """Represents Signal's Vessel Valuation API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Vessel Valuations API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_latest_valuation_price(self, imo: int) -> Optional[Decimal]:
        """Retrieves the latest valuation price (in $M) for a specific vessel.

        Args:
            imo: The IMO number of the vessel.

        Returns:
            A Decimal representing the valuation price or None if a vessel
            with the given IMO number does not exist or has no valuation.
        """
        return self.__get(
            f"valuations/SnPValuation/lastvaluation/{imo}",
            lambda response: as_decimal(response.text),
        )

    def get_latest_valuation(self, imo: int) -> Optional[Valuation]:
        """Retrieves the latest valuation for a specific vessel.

        Args:
            imo: The IMO number of the vessel.

        Returns:
            A valuation or None if a vessel with the given IMO number does not
            exist or has no valuation.
        """
        return self.__get(
            f"valuations/SnPValuation/lastvaluation/shortdetails/{imo}",
            lambda response: _valuation_json.parse_valuation(response.json()),
        )

    def get_valuations(self, imo: int) -> Optional[Tuple[Valuation, ...]]:
        """Retrieves all valuations for a specific vessel.

        Args:
            imo: The IMO number of the vessel.

        Returns:
            A tuple of valuations or None if a vessel with the given IMO number
            does not exist.
        """
        return self.__get(
            f"valuations/SnPValuation/allvaluations/shortdetails/{imo}",
            lambda response: _valuation_json.parse_valuations(response.json()),
        )

    def __get(
        self,
        relative_url: str,
        parse_response: Callable[[requests.Response], TValuation],
    ) -> Optional[TValuation]:
        response = self.__connection._make_get_request(relative_url)
        if response.status_code == requests.codes.not_found:
            return None

        response.raise_for_status()
        return parse_response(response)
