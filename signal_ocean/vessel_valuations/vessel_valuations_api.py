# noqa: D100

from decimal import Decimal
from urllib.parse import urljoin
from typing import Optional, Callable, TypeVar

import requests

from .models import ValuationSummary, ValuationHistory
from . import _valuation_json
from ..connection import Connection
from .._internals import as_decimal

TValuation = TypeVar('TValuation')


class VesselValuationsAPI:
    """Represents Signal's Vessel Valuation API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Vessel Valuations API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_latest_valuation(self, imo: int) -> Optional[Decimal]:
        """Retrieves the latest valuation (in $M) for a specific vessel.
                
        Args:
            imo: The IMO number of the vessel.

        Returns:
            A Decimal representing the valuation value or None if a vessel
            with the given IMO number does not exist or has no valuation.
        """
        return self.__get(
            f'valuations/SnPValuation/lastvaluation/{imo}',
            lambda response: as_decimal(response.text)
        )

    def get_latest_valuation_summary(self, imo: int) -> Optional[ValuationSummary]:
        """Retrieves the latest valuation summary for a specific vessel.
                
        Args:
            imo: The IMO number of the vessel.

        Returns:
            An instance of ValuationSummary or None if a vessel with
            the given IMO number does not exist or has no valuation.
        """
        return self.__get(
            f'valuations/SnPValuation/lastvaluation/shortdetails/{imo}',
            lambda response: _valuation_json.parse_summary(response.json())
        )

    def get_valuation_history(self, imo: int) -> Optional[ValuationHistory]:
        """Retrieves all valuation summaries for a specific vessel.
                
        Args:
            imo: The IMO number of the vessel.

        Returns:
            An instance of ValuationHistory or None if a vessel with
            the given IMO number does not exist or has no valuation.
        """
        return self.__get(
            f'valuations/SnPValuation/allvaluations/shortdetails/{imo}',
            lambda response: _valuation_json.parse_valuation_history(response.json())
        )

    def __get(
            self,
            relative_url: str,
            parse_response: Callable[[requests.Response], TValuation]) -> Optional[TValuation]:
        url = urljoin(self.__connection._api_host, relative_url)

        response = requests.get(url, headers=self.__connection._headers)
        if (response.status_code == requests.codes.not_found):
            return None

        response.raise_for_status()
        return parse_response(response)
