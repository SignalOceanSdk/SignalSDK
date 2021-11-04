"""The oilx cargo tracking api."""
from typing import Optional, Tuple, List
from urllib.parse import urljoin

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single
from signal_ocean.oilx_cargo_tracking.oilx_models import (
    CargoFlow,
    CargoFlowsPagedResponse,
)

CargoFlows = Tuple[CargoFlow, ...]
NextRequestToken = str


class OilxCargoTrackingAPI:
    """Represents OilX Cargo Tracking API."""

    relative_url = "oilx-cargo-tracking-api/v1/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes OilxCargoTrackingAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    @staticmethod
    def _get_endpoint(
        vessel_class_id: Optional[int] = None, incremental: bool = False
    ) -> str:
        """Retrieves the endpoint to call to retrieve the requested cargo flows.

        Args:
            vessel_class_id:
                Return only cargo flows for the provided vessel class.
                If None, cargo flows for all vessels are returned.
            incremental: Return cargo flows incrementally.

        Returns:
            The endpoint to call to retrieve the requested cargo flows for
            the provided arguments.
        """
        endpoint = "cargoTracking"

        if vessel_class_id is not None:
            endpoint += f"/class/{vessel_class_id}"
        if incremental:
            endpoint += "/incremental"

        return urljoin(OilxCargoTrackingAPI.relative_url, endpoint)

    def _get_oilx_cargoes_pages(
        self, endpoint: str, token: Optional[str] = None
    ) -> Tuple[CargoFlows, Optional[NextRequestToken]]:
        """Get cargo flows paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental cargo flows.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Cargo flows data gathered from the returned pages.
        """
        results: List[CargoFlow] = []
        next_page_token = token
        while True:
            params = (
                {"token": next_page_token}
                if next_page_token is not None
                else None
            )
            response = get_single(
                self.__connection,
                endpoint,
                CargoFlowsPagedResponse,
                query_string=params,
                rename_keys={'APIGravity': 'ApiGravity'}
            )

            if response is not None and response.data is not None:
                results.extend(response.data)

            next_page_token = (
                response.next_page_token if response is not None else None
            )

            if next_page_token is None:
                break

        next_request_token = (
            response.next_request_token if response is not None else None
        )
        return tuple(results), next_request_token

    def get_oilx_cargoes(
        self,
        vessel_class_id: Optional[int] = None,
        incremental_token: Optional[str] = None
    ) -> Tuple[CargoFlows, Optional[str]]:
        """Retrieves all cargo flows filtered for the provided parameters.

        Args:
            vessel_class_id:
                Return only cargo flows for the provided vessel class.
                If None, cargo flows for all vessels are returned.

        Returns:
            A tuple containing the returned cargo flows.
        """
        if incremental_token is not None:
            endpoint = self._get_endpoint(vessel_class_id, incremental=True)
        else:
            endpoint = self._get_endpoint(vessel_class_id, incremental=False)

        results, next_request_token = self._get_oilx_cargoes_pages(
            endpoint, token=incremental_token
        )

        return results, next_request_token
