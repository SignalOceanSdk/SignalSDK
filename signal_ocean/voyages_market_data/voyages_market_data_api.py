"""The voyages api."""
from datetime import date
from typing import Optional, Tuple, List
from urllib.parse import urljoin, urlencode

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single, get_multiple
from signal_ocean.util.parsing_helpers import _to_camel_case
from signal_ocean.voyages_market_data.models import (
    VoyagesMarketData,
    VoyagesMarketDataPagedResponse,
)

VoyagesMarketDataMultiple = Tuple[VoyagesMarketData, ...]
NextRequestToken = str


class VoyagesMarketDataAPI:
    """Represents Signal's VoyagesMarketData API."""

    relative_url = "voyages-market-data-api/v1/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VoyagesMarketDataAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    @staticmethod
    def _get_endpoint(
        imo: Optional[int] = None,
        voyage_id: Optional[int] = None,
        voyage_number: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        incremental: Optional[date] = None,
        include_vessel_details: Optional[bool] = None,
        include_fixtures: Optional[bool] = None,
        include_matched_fixture: Optional[bool] = None,
        include_labels: Optional[bool] = None
    ) -> str:
        """Retrieves the endpoint to call to construct the request.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            voyage_id: If provided only market data with the requested voyage
                ID will be returned.
            voyage_number: If provided only market data with the requested
                voyageNumber will be returned.
            vessel_class_id: If provided only market data with the requested
                vesselClassId will be returned.
            vessel_type_id: If provided only market data with the requested
                vesselTypeId will be returned. Potential values are 0-> Empty,
                1-> Tanker, 3-> Dry, 4-> Container, 5-> Lng, 6-> Lpg,
                -2-> NotSet, -1-> Unknown
            incremental:  Return voyages incrementally, including voyages that
                may have been retrieved in previous calls and are now deleted.
            include_vessel_details: If set to true the following fields will
                be included in the response. VesselName, Deadweight,
                YearBuilt, VesselClass, VesselType, Trade, CommercialOperator
            include_fixtures: If True, information on fixtures will be
                included in the response.
            include_matched_fixture: If True, information on the matched
                fixture will be included in the response.
            include_labels: If set to true the following fields will be
                included in the response. Charterer, LoadName, LoadTaxonomy,
                LoadName2, LoadTaxonomy2, DischargeName, DischargeTaxonomy,
                DischargeName2, DischargeTaxonomy2, CargoType, CargoGroup,
                CargoGroupID, DeliveryName, DeliveryTaxonomy,
                RedeliveryFromName, RedeliveryFromTaxonomy, RedeliveryToName,
                RedeliveryToTaxonomy
        Returns:
            The endpoint to call to retrieve the requested voyage market \
            data for the provided arguments.
        """
        endpoint_params = {}

        for key, value in locals().items():
            if key in {'include_vessel_details', 'include_fixtures',
                       'include_matched_fixture', 'include_labels'}:
                endpoint_params[key] = value

        endpoint = "marketData"

        if imo is not None:
            endpoint += f"/imo/{imo}"
            if voyage_number is not None:
                endpoint += f"/voyage/{voyage_number}"
        elif voyage_id is not None:
            endpoint += f"/type/{voyage_id}"
        elif vessel_class_id is not None:
            endpoint += f"/class/{vessel_class_id}"
        elif vessel_type_id is not None:
            endpoint += f"/type/{vessel_type_id}"
        else:
            raise NotImplementedError(
                "please provide at least one of the following arguments: "
                "imo, voyage_number, voyage_id, vessel_class_id, "
                "vessel_type_id")

        if imo is None and incremental is not None:
            endpoint += f"/incremental/{incremental}"

        endpoint += "?"

        params = urlencode(
            {
                _to_camel_case(key): value
                for key, value in endpoint_params.items()
                if value is not None
            }
        )
        endpoint += params

        return urljoin(VoyagesMarketDataAPI.relative_url, endpoint)

    def _get_voyage_market_data_pages(
        self, endpoint: str, token: Optional[str] = None
    ) -> Tuple[VoyagesMarketDataMultiple, Optional[NextRequestToken]]:
        """Retrieves data filtered for the provided parameters.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyage market data.
                Make consecutive requests until no next page token is
                returned, gather and return data.

        Returns:
            Voyage market data gathered from the returned pages.
            The next request token, to be used for incremental updates.
        """
        results: List[VoyagesMarketData] = []
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
                VoyagesMarketDataPagedResponse,
                query_string=params,
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

    def get_voyage_market_data(
        self,
        imo: Optional[int] = None,
        voyage_id: Optional[int] = None,
        voyage_number: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        incremental: Optional[date] = None,
        include_vessel_details: Optional[bool] = None,
        include_fixtures: Optional[bool] = None,
        include_matched_fixture: Optional[bool] = None,
        include_labels: Optional[bool] = None
    ) -> VoyagesMarketDataMultiple:
        """Retrieves market data filtered for the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            voyage_id: If provided only market data with the requested voyage
                ID will be returned.
            voyage_number: If provided only market data with the requested
                voyageNumber will be returned.
            vessel_class_id: If provided only market data with the requested
                vesselClassId will be returned.
            vessel_type_id: If provided only market data with the requested
                vesselTypeId will be returned. Potential values are 0-> Empty,
                1-> Tanker, 3-> Dry, 4-> Container, 5-> Lng, 6-> Lpg,
                -2-> NotSet, -1-> Unknown
            incremental:  Return voyages incrementally, including voyages that
                may have been retrieved in previous calls and are now deleted.
            include_vessel_details: If set to true the following fields will
                be included in the response. VesselName, Deadweight,
                YearBuilt, VesselClass, VesselType, Trade, CommercialOperator
            include_fixtures: If True, information on fixtures will be
                included in the response.
            include_matched_fixture: If True, information on the matched
                fixture will be included in the response.
            include_labels: If set to true the following fields will be
                included in the response. Charterer, LoadName, LoadTaxonomy,
                LoadName2, LoadTaxonomy2, DischargeName, DischargeTaxonomy,
                DischargeName2, DischargeTaxonomy2, CargoType, CargoGroup,
                CargoGroupID, DeliveryName, DeliveryTaxonomy,
                RedeliveryFromName, RedeliveryFromTaxonomy, RedeliveryToName,
                RedeliveryToTaxonomy
        Returns:
            A tuple containing the returned voyage market data.
        """
        endpoint = self._get_endpoint(
                        imo, voyage_id, voyage_number, vessel_class_id,
                        vessel_type_id, incremental, include_vessel_details,
                        include_fixtures, include_matched_fixture,
                        include_labels
        )

        if imo is not None:
            results = get_multiple(self.__connection, endpoint,
                                   VoyagesMarketData, data_key_label='Data')
        else:
            results, _ = self._get_voyage_market_data_pages(endpoint)

        return results
