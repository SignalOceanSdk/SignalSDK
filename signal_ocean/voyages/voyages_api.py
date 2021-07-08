"""The voyages api."""
from datetime import date
from typing import Optional, Tuple, List
from urllib.parse import urljoin, urlencode

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single, get_multiple
from signal_ocean.util.parsing_helpers import _to_camel_case
from signal_ocean.voyages.models import Voyage, VoyagesFlat, \
    VoyagesFlatPagedResponse, VoyageEvent, \
    VoyageEventDetail, VoyageGeo, VoyagesPagedResponse

Voyages = Tuple[Voyage, ...]
NextRequestToken = str


class VoyagesAPI:
    """Represents Signal's Voyages API."""

    relative_url = "voyages-api/v2/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VoyagesAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    @staticmethod
    def _get_endpoint(imo: Optional[int] = None,
                      vessel_class_id: Optional[int] = None,
                      vessel_type_id: Optional[int] = None,
                      date_from: Optional[date] = None,
                      nested: Optional[bool] = True,
                      incremental: bool = False) -> str:
        """Retrieves the endpoint to call to retrieve the requested voyages.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None, voyages for all vessels are returned. If imo is
                specified vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, voyages for all vessels are returned. If either imo
                or vessel_class_id is specified vessel_type_id is ignored.
            date_from: Return voyages after provided date. If imo is specified
                date_from is treated as None.
            nested: Boolean controlling whether information associated with
                voyages is returned nested in the voyage object or in flat
                format.
            incremental: Return voyages incrementally, including voyages that
                may have been retrieved in previous calls and are now deleted.

        Returns:
            The endpoint to call to retrieve the requested voyages for
            the provided arguments.
        """
        endpoint = f'voyages{"" if nested else "flat"}'

        if imo is not None:
            endpoint += f'/imo/{imo}'
        elif vessel_class_id is not None:
            endpoint += f'/class/{vessel_class_id}'
        elif vessel_type_id is not None and \
                (date_from is not None or incremental):
            endpoint += f'/type/{vessel_type_id}'
        elif not incremental:
            raise NotImplementedError('For non incremental mode, either imo, '
                                      'vessel_class_id or both vessel_type_id '
                                      'and date_from must be provide.')

        if imo is None and date_from is not None:
            endpoint += f'/date/{date_from.isoformat()}'

        if incremental:
            endpoint += '/incremental'

        return urljoin(VoyagesAPI.relative_url, endpoint)

    @staticmethod
    def _get_advanced_endpoint(
                        event_type: Optional[int] = None,
                        event_horizon: Optional[int] = None,
                        event_purpose: Optional[str] = None,
                        vessel_class_id: Optional[int] = None,
                        vessel_type_id: Optional[int] = None,
                        start_date_from:  Optional[date] = None,
                        start_date_to: Optional[date] = None,
                        first_load_arrival_date_from: Optional[date] = None,
                        first_load_arrival_date_to: Optional[date] = None,
                        end_date_from: Optional[date] = None,
                        end_date_to: Optional[date] = None,
                        market_info_rate_from: Optional[date] = None,
                        market_info_rate_to: Optional[date] = None,
                        market_info_rate_type: Optional[date] = None,
                        commercial_operator_id: Optional[int] = None,
                        charterer_id: Optional[int] = None,
                        voyage_horizon: Optional[str] = None,
                        token: Optional[str] = None,
                        hide_event_details: Optional[bool] = None,
                        hide_events: Optional[bool] = None,
                        hide_market_info: Optional[bool] = None) -> str:
        """Constructs the advanced search endpoint.

        Args:
            endpoint_params: Advanced search endpoint parameters dictionary.
            Same as get_voyages_by_advanced_search method arguments.

        Returns:
            The constructed endpoint to call to retrieve the requested voyages
            for the provided arguments.
        """
        endpoint_params = locals()
        endpoint = 'search/advanced/?'
        params = urlencode({_to_camel_case(key): value for key, value
                            in endpoint_params.items() if value is not None})
        endpoint += params
        return urljoin(VoyagesAPI.relative_url, endpoint)

    def _get_voyages_pages(self, endpoint: str, token: Optional[str] = None) \
            -> Tuple[Voyages, Optional[NextRequestToken]]:
        """Get voyages paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyages.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Voyages data gathered from the returned pages.
        """
        results: List[Voyage] = []
        next_page_token = token
        while True:
            params = {'token': next_page_token} \
                if next_page_token is not None else None
            response = get_single(self.__connection, endpoint,
                                  VoyagesPagedResponse, query_string=params)
            if response is not None and response.data is not None:
                results.extend(response.data)
            next_page_token = response.next_page_token \
                if response is not None else None

            if next_page_token is None:
                break

        next_request_token = response.next_request_token \
            if response is not None else None
        return tuple(results), next_request_token

    def _get_voyages_flat_pages(self, endpoint: str,
                                token: Optional[str] = None) \
            -> Tuple[VoyagesFlat, Optional[NextRequestToken]]:
        """Get voyages flat paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyages.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Voyages flat data gathered from the returned pages.
        """
        voyages: List[Voyage] = []
        events: List[VoyageEvent] = []
        event_details: List[VoyageEventDetail] = []
        geos: List[VoyageGeo] = []
        next_page_token = token
        while True:
            params = {'token': next_page_token} \
                if next_page_token is not None else None

            response = get_single(self.__connection,
                                  endpoint,
                                  VoyagesFlatPagedResponse,
                                  query_string=params)

            if response is not None and response.data is not None:
                voyages.extend(response.data.voyages or [])
                events.extend(response.data.events or [])
                event_details.extend(
                    response.data.event_details or [])
                geos.extend(response.data.geos or [])

            next_page_token = response.next_page_token \
                if response is not None else None

            if next_page_token is None:
                break

        result = VoyagesFlat(voyages=tuple(voyages), events=tuple(events),
                             event_details=tuple(event_details),
                             geos=tuple(geos))

        next_request_token = response.next_request_token \
            if response is not None else None

        return result, next_request_token

    def get_voyages(self,
                    imo: Optional[int] = None,
                    vessel_class_id: Optional[int] = None,
                    vessel_type_id: Optional[int] = None,
                    date_from: Optional[date] = None) \
            -> Voyages:
        """Retrieves all voyages filtered for the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None voyages for all vessels are returned. If imo is
                specified and vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None voyages for all vessels are returned. If either imo or
                vessel_class_id is specified vessel_type_id is ignored.
            date_from: Return voyages after provided date. If imo is specified
                date_from is treated as None.

        Returns:
            A tuple containing the returned voyages.
        """
        endpoint = self._get_endpoint(imo, vessel_class_id, vessel_type_id,
                                      date_from, nested=True)
        if imo is not None:
            results = get_multiple(self.__connection, endpoint, Voyage)
        else:
            results, _ = self._get_voyages_pages(endpoint)
        return results

    def get_voyages_flat(self,
                         imo: Optional[int] = None,
                         vessel_class_id: Optional[int] = None,
                         vessel_type_id: Optional[int] = None,
                         date_from: Optional[date] = None) \
            -> Optional[VoyagesFlat]:
        """Retrieves all voyages filtered for the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None voyages for all vessels are returned. If imo is
                specified and vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None voyages for all vessels are returned. If either imo or
                vessel_class_id is specified vessel_type_id is ignored.
            date_from: Return voyages after provided date. If imo is specified
                date_from is treated as None.

        Returns:
            A VoyagesFlat object containing lists of voyages, voyage events,
            voyage event details and voyage geos otherwise.
        """
        endpoint = self._get_endpoint(imo, vessel_class_id, vessel_type_id,
                                      date_from, nested=False)
        if imo is not None:
            results = get_single(self.__connection, endpoint, VoyagesFlat)
        else:
            results, _ = self._get_voyages_flat_pages(endpoint)

        return results

    def get_incremental_voyages(self,
                                imo: Optional[int] = None,
                                vessel_class_id: Optional[int] = None,
                                vessel_type_id: Optional[int] = None,
                                date_from: Optional[date] = None,
                                incremental_token: Optional[str] = None)\
            -> Tuple[Voyages, Optional[NextRequestToken]]:
        """Retrieves all voyages filtered for the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None voyages for all vessels are returned. If imo is
                specified and vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None voyages for all vessels are returned. If either imo or
                vessel_class_id is specified vessel_type_id is ignored.
            date_from: Return voyages after provided date. If imo is specified
                date_from is treated as None.
            incremental_token: Token returned from the previous incremental
                call. If this is the first call, then it can be omitted.

        Returns:
            A tuple containing the returned voyages, including any deleted
            voyages, and the token for the next incremental request.
        """
        endpoint = self._get_endpoint(imo, vessel_class_id, vessel_type_id,
                                      date_from, nested=True, incremental=True)
        results = self._get_voyages_pages(endpoint, token=incremental_token)
        return results

    def get_incremental_voyages_flat(self,
                                     imo: Optional[int] = None,
                                     vessel_class_id: Optional[int] = None,
                                     vessel_type_id: Optional[int] = None,
                                     date_from: Optional[date] = None,
                                     incremental_token: Optional[str] = None)\
            -> Tuple[VoyagesFlat, Optional[NextRequestToken]]:
        """Retrieves all voyages filtered for the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None voyages for all vessels are returned. If imo is
                specified and vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None voyages for all vessels are returned. If either imo or
                vessel_class_id is specified vessel_type_id is ignored.
            date_from: Return voyages after provided date. If imo is specified
                date_from is treated as None.
            incremental_token: Token returned from the previous incremental
                call. If this is the first call, then it can be omitted.

        Returns:
            A tuple containing the returned voyages in flat format, including
            any deleted voyages, and the token for the next incremental
            request.
        """
        endpoint = self._get_endpoint(imo, vessel_class_id, vessel_type_id,
                                      date_from, nested=False,
                                      incremental=True)
        results = self._get_voyages_flat_pages(endpoint,
                                               token=incremental_token)
        return results

    def get_voyages_by_advanced_search(
                        self,
                        event_type: Optional[int] = None,
                        event_horizon: Optional[int] = None,
                        event_purpose: Optional[str] = None,
                        vessel_class_id: Optional[int] = None,
                        vessel_type_id: Optional[int] = None,
                        start_date_from:  Optional[date] = None,
                        start_date_to: Optional[date] = None,
                        first_load_arrival_date_from: Optional[date] = None,
                        first_load_arrival_date_to: Optional[date] = None,
                        end_date_from: Optional[date] = None,
                        end_date_to: Optional[date] = None,
                        market_info_rate_from: Optional[date] = None,
                        market_info_rate_to: Optional[date] = None,
                        market_info_rate_type: Optional[date] = None,
                        commercial_operator_id: Optional[int] = None,
                        charterer_id: Optional[int] = None,
                        voyage_horizon: Optional[str] = None,
                        token: Optional[str] = None,
                        hide_event_details: Optional[bool] = None,
                        hide_events: Optional[bool] = None,
                        hide_market_info: Optional[bool] = None) -> Voyages:
        """Retrieves all voyages filtered for the provided parameters.

        Args:
            event_type: If an EventType is provided then only voyages that
                include at least one event of this type will be returned.
            event_horizon: If an EventHorizon is provided then only voyages
                that include at least one event of this type will be returned.
            event_purpose: If an EventPurpose is provided then only voyages
                that include at least one event of this type will be returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None voyages for all vessels are returned.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None voyages for all vessels are returned.
            start_date_from: Return voyages after the provided voyage start
                date.
            start_date_to: Return voyages up to the provided voyage end date.

            first_load_arrival_date_from: Return voyages with a first load
                arrival date after the provided date.
            first_load_arrival_date_to: Return voyages with a first load
                arrival date up to the provided date.
            end_date_from: Return voyages after the provided voyage end date.

            end_date_to: Return voyages up to the provided voyage end date.

            market_info_rate_from: If provided only voyages that have market
                data and with rate greater than this will be returned.
            market_info_rate_to: If provided only voyages that have market data
                and with rate lower than this will be returned.
            market_info_rate_type: If provided only voyages that have market
                data and with rate type equal to this will be returned.
            commercial_operator_id: If provided only voyages that have this
                commercial operator will be returned.
            charterer_id: If provided only voyages that have this charterer
                will be returned.
            voyage_horizon: If a VoyageHorizon is provided then only voyages
                of that type will be returned.
            token: Token returned from the previous incremental call. If this
                is the first call, then it can be omitted.
            hide_event_details: If True, do not return event details.

            hide_events: If True, do not return events.

            hide_market_info: If True, do not return market information.

        Returns:
            A tuple containing the returned voyages.
        """
        endpoint = self._get_advanced_endpoint(
            event_type=event_type, event_horizon=event_horizon,
            event_purpose=event_purpose, vessel_class_id=vessel_class_id,
            vessel_type_id=vessel_type_id, start_date_from=start_date_from,
            start_date_to=start_date_to,
            first_load_arrival_date_from=first_load_arrival_date_from,
            first_load_arrival_date_to=first_load_arrival_date_to,
            end_date_from=end_date_from, end_date_to=end_date_to,
            market_info_rate_from=market_info_rate_from,
            market_info_rate_to=market_info_rate_to,
            market_info_rate_type=market_info_rate_type,
            commercial_operator_id=commercial_operator_id,
            charterer_id=charterer_id, voyage_horizon=voyage_horizon,
            token=token, hide_event_details=hide_event_details,
            hide_events=hide_events, hide_market_info=hide_market_info)

        results, _ = self._get_voyages_pages(endpoint)
        return results
