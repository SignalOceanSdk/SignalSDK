"""The voyages api."""
from datetime import date
from typing import Optional, Tuple, List
from urllib.parse import urljoin, urlencode

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single
from signal_ocean.util.parsing_helpers import _to_camel_case, parse_model
from signal_ocean.voyages.models import (
    Voyage,
    VoyageCondensed,
    VoyagesCondensedPagedResponse,
    VoyagesFlat,
    VoyagesFlatPagedResponse,
    VoyageEvent,
    VoyageEventDetail,
    VoyageGeo,
    VoyagesPagedResponse,
    VesselClassFilter,
    VesselClass,
    VesselTypeFilter,
    VesselType,
    Vessel,
    VesselFilter,
)

Voyages = Tuple[Voyage, ...]
VoyagesCondensed = Tuple[VoyageCondensed, ...]
NextRequestToken = str


class VoyagesAPI:
    """Represents Signal's Voyages API."""

    relative_url = "voyages-api/v4/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VoyagesAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    @staticmethod
    def _get_endpoint(
        imo: Optional[List[int]] = None,
        voyage_keys: Optional[List[str]] = None,
        event_type: Optional[int] = None,
        event_horizons: Optional[List[int]] = None,
        event_purpose: Optional[List[str]] = None,
        vessel_class_id: Optional[List[int]] = None,
        port_ids: Optional[List[int]] = None,
        vessel_type_id: Optional[int] = None,
        voyage_date_from: Optional[date] = None,
        voyage_date_to: Optional[date] = None,
        voyage_number_from: Optional[int] = None,
        voyage_number_to: Optional[int] = None,
        start_date_from: Optional[date] = None,
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
        voyage_horizon: Optional[List[str]] = None,
        token: Optional[str] = None,
        hide_event_details: Optional[bool] = None,
        hide_events: Optional[bool] = None,
        hide_market_info: Optional[bool] = None,
        nested: Optional[bool] = True,
        condensed: Optional[bool] = False,
        incremental: Optional[bool] = False,
    ) -> str:
        """Constructs the VoyagesData v4 endpoint.

        Args:
            endpoint_params: VoyagesData v4 endpoint parameters dictionary.
            Part of get_voyages method arguments.
            Part of get_voyages_incremental arguments.

        Returns:
            The constructed endpoint to call to retrieve the requested \
            voyages for the provided arguments.
        """
        # Special Handling for event purposes and VoyageHorizons
        endpoint_params = locals()
        if condensed:
            format_type = "condensed"
        elif nested:
            format_type = "nested"
        else:
            format_type = "flat"
        endpoint = "voyages/" + \
            format_type + \
            f'{"/incremental?" if incremental else "?"}'

        del endpoint_params["nested"]
        del endpoint_params["condensed"]
        del endpoint_params["incremental"]
        params = urlencode(
            {
                _to_camel_case(key): value
                for key, value in endpoint_params.items()
                if value is not None and value is not []
            }, doseq=True
        )
        endpoint += params
        return urljoin(VoyagesAPI.relative_url, endpoint)

    def _get_voyages_pages(
        self, endpoint: str, token: Optional[str] = None
    ) -> Tuple[Voyages, Optional[NextRequestToken]]:
        """Get voyages paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyages.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Voyages data gathered from the returned pages as a tupple.
            The next request token, to be used for incremental updates.
        """
        results: List[Voyage] = []
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
                VoyagesPagedResponse,
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

    def _get_voyages_flat_pages(
        self, endpoint: str, token: Optional[str] = None
    ) -> Tuple[VoyagesFlat, Optional[NextRequestToken]]:
        """Get voyages flat paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyages.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Voyages flat data gathered from the returned pages as a tupple.
            The next request token, to be used for incremental updates.
        """
        voyages: List[Voyage] = []
        events: List[VoyageEvent] = []
        event_details: List[VoyageEventDetail] = []
        geos: List[VoyageGeo] = []
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
                VoyagesFlatPagedResponse,
                query_string=params,
            )

            if response is not None and response.data is not None:
                voyages.extend(response.data.voyages or [])
                events.extend(response.data.events or [])
                event_details.extend(response.data.event_details or [])
                geos.extend(response.data.geos or [])

            next_page_token = (
                response.next_page_token if response is not None else None
            )

            if next_page_token is None:
                break

        # Remove duplicate geos entries because of the multiple paging
        geos = list({geo.id: geo for geo in geos}.values())

        result = VoyagesFlat(
            voyages=tuple(voyages),
            events=tuple(events),
            event_details=tuple(event_details),
            geos=tuple(geos),
        )

        next_request_token = (
            response.next_request_token if response is not None else None
        )

        return result, next_request_token

    def _get_voyages_condensed_pages(
        self, endpoint: str, token: Optional[str] = None
    ) -> Tuple[VoyagesCondensed, Optional[NextRequestToken]]:
        """Get voyages condensed paged data.

        Args:
            endpoint: The endpoint to call.
            token: Next request token for incremental voyages.

        Make consecutive requests until no next page token is returned, gather
        and return data.

        Returns:
            Voyages condensed data gathered from the returned pages as a
            tupple. The next request token, for incremental updates.
        """
        results: List[VoyageCondensed] = []
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
                VoyagesCondensedPagedResponse,
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

    def get_voyages(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
    ) -> Voyages:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None,
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, voyages for all vessels are returned. If
                imo is specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, voyages for all vessels are returned. If either imo
                or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return voyages after provided date. If imo is
                specified, then date_from is ignored.

        Returns:
            Voyages data as a tupple.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []

        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            start_date_from=date_from
        )
        results, _ = self._get_voyages_pages(endpoint)
        return results

    def get_voyages_flat(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
    ) -> Optional[VoyagesFlat]:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, voyages for all vessels are returned. If imo
                is specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, voyages for all vessels are returned. If either imo
                or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return voyages after provided date. If imo is
                specified, then date_from is treated as None.

        Returns:
            A VoyagesFlat object containing lists of voyages, voyage events, \
            voyage event details and voyage geos otherwise.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []

        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            start_date_from=date_from,
            nested=False
        )
        results, _ = self._get_voyages_flat_pages(endpoint)
        return results

    def get_voyages_condensed(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
    ) -> VoyagesCondensed:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None
                voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, voyages for all vessels are returned. If imo
                is specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, voyages for all vessels are returned. If either imo
                or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return voyages after provided date. If imo is
                specified, then date_from is treated as None.

        Returns:
            A VoyagesCondensed object containing lists of voyages.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []
        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            start_date_from=date_from,
            nested=False,
            condensed=True
        )
        results, _ = self._get_voyages_condensed_pages(endpoint)
        return results

    def get_incremental_voyages(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
        incremental_token: Optional[str] = None,
    ) -> Tuple[Voyages, Optional[NextRequestToken]]:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None,
                then voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, then voyages for all vessels are returned. If
                imo is specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, then voyages for all vessels are returned. If either
                imo or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return voyages after provided date. If imo is
                specified, then date_from is treated as None.
            incremental_token: Token returned from the previous incremental
                call. If this is the first call, then it can be omitted.

        Returns:
            A tuple containing the returned voyages, including any deleted \
            voyages, and the token for the next incremental request.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []
        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            voyage_date_from=date_from,
            nested=True,
            incremental=True
        )
        results = self._get_voyages_pages(endpoint, token=incremental_token)
        return results

    def get_incremental_voyages_flat(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
        incremental_token: Optional[str] = None,
    ) -> Tuple[VoyagesFlat, Optional[NextRequestToken]]:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None,
                then voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, voyages for all vessels are returned. If imo
                is specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, voyages for all vessels are returned. If either imo
                or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return  after the provided date. If imo is
                specified, then datevoyages_from is treated as None.
            incremental_token: Token returned from the previous incremental
                call. If this is the first call, then it can be omitted.

        Returns:
            A tuple containing the returned voyages in flat format, \
            including any deleted voyages, and the token for the next \
            incremental request.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []
        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            voyage_date_from=date_from,
            nested=False,
            incremental=True
        )
        results = self._get_voyages_flat_pages(
            endpoint, token=incremental_token
        )
        return results

    def get_incremental_voyages_condensed(
        self,
        imo: Optional[int] = None,
        vessel_class_id: Optional[int] = None,
        vessel_type_id: Optional[int] = None,
        date_from: Optional[date] = None,
        incremental_token: Optional[str] = None,
    ) -> Tuple[VoyagesCondensed, Optional[NextRequestToken]]:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imo: Return only voyages for the provided vessel IMO. If None,
                then voyages for all vessels are returned.
            vessel_class_id: Return only voyages for the provided vessel class.
                If None, then voyages for all vessels are returned. If imo is
                specified, then vessel_class_id is ignored.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, then voyages for all vessels are returned. If either
                imo or vessel_class_id is specified, then vessel_type_id is
                ignored.
            date_from: Return voyages after provided date. If imo is
                specified, then date_from is treated as None.
            incremental_token: Token returned from the previous incremental
                call. If this is the first call, then it can be omitted.

        Returns:
            A tuple containing the returned voyages in condensed format, \
            including any deleted voyages, and the token for the next \
            incremental request.
        """
        if vessel_class_id is not None:
            vcids = [vessel_class_id]
        else:
            vcids = []

        if imo is not None:
            imos = [imo]
        else:
            imos = []
        endpoint = self._get_endpoint(
            imo=imos,
            vessel_class_id=vcids,
            vessel_type_id=vessel_type_id,
            voyage_date_from=date_from,
            nested=False,
            incremental=True,
            condensed=True
        )
        results = self._get_voyages_condensed_pages(
            endpoint, token=incremental_token
        )
        return results

    def get_voyages_by_advanced_search(
        self,
        imos: Optional[List[int]] = None,
        voyage_keys: Optional[List[str]] = None,
        event_type: Optional[int] = None,
        event_horizon: Optional[int] = None,
        event_horizons: Optional[List[int]] = None,
        event_purpose: Optional[str] = None,
        event_purposes: Optional[List[str]] = None,
        vessel_class_id: Optional[int] = None,
        vessel_class_ids: Optional[List[int]] = None,
        port_id: Optional[int] = None,
        port_ids: Optional[List[int]] = None,
        vessel_type_id: Optional[int] = None,
        start_date_from: Optional[date] = None,
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
        voyage_horizons: Optional[List[str]] = None,
        token: Optional[str] = None,
        hide_event_details: Optional[bool] = None,
        hide_events: Optional[bool] = None,
        hide_market_info: Optional[bool] = None,
    ) -> Voyages:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imos: If a list of imos is provided then only voyages of these
                imos will be returned
            voyage_keys: If provided only the voyages with the requested
                keys will be returned
            event_type: If an EventType is provided, then only voyages that
                include at least one event of this type will be returned.
            event_horizon: If an EventHorizon is provided, then only voyages
                of this event horizon will be returned.
            event_horizons: If a list of EventHorizons is provided then only
                voyages that include at least one event of those types
                will be returned
            event_purpose: If an EventPurpose is provided, then only voyages
                that include at least one event of this purpose will be
                returned.
            event_purposes: If a list of EventPurposes is provided then only
                voyages that include at least one event of this type
                will be returned
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, then voyages for all vessels are returned.
            vessel_class_ids: If provided only voyages of those vessel classes
                will be returned.
            port_id: If PortId is provided then only voyages that contains at
                least one event at this port will be returned.
            port_ids: If a list of ports is provided then only voyages that
                contains at least one event at those ports will be returned.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, then voyages for all vessels are returned.
            start_date_from: Return voyages after the provided voyage start
                date.
            start_date_to: Return voyages up to the provided voyage end date.
            first_load_arrival_date_from: Return voyages with a first load
                arrival date after the provided date.
            first_load_arrival_date_to: Return voyages with a first load
                arrival date up to the provided date.
            end_date_from: Return voyages with an end date after the provided
                date.
            end_date_to: Return voyages with an end date up to the provided
                date.
            market_info_rate_from: If provided, then only voyages that have
                market data and with rate greater than this will be returned.
            market_info_rate_to: If provided, then only voyages that have
                market data and with a lower rate will be returned.
            market_info_rate_type: If provided, then only voyages that have
                market data and with the same rate type will be returned.
            commercial_operator_id: If provided, then only voyages that have
                this commercial operator will be returned.
            charterer_id: If provided, then only voyages that have this
                charterer will be returned.
            voyage_horizon: If a VoyageHorizon is provided, then only voyages
                of that type will be returned.
            voyage_horizons: If a list of VoyageHorizon is provided then
                only voyages of that type will be returned.
            token: Token returned from the previous incremental call. If this
                is the first call, then it can be omitted.
            hide_event_details: If True, then event details will be excluded.
            hide_events: If True, then events will be excluded.
            hide_market_info: If True, then market information will be
                excluded.

        Returns:
            Voyages data as a tupple.
        """
        if event_horizon is not None:
            if event_horizons is None:
                event_horizons = []
            event_horizons.append(event_horizon)

        if event_purpose is not None:
            if event_purposes is None:
                event_purposes = []
            event_purposes.append(event_purpose)

        if vessel_class_id is not None:
            if vessel_class_ids is None:
                vessel_class_ids = []
            vessel_class_ids.append(vessel_class_id)

        if port_id is not None:
            if port_ids is None:
                port_ids = []
            port_ids.append(port_id)

        if voyage_horizon is not None:
            if voyage_horizons is None:
                voyage_horizons = []
            voyage_horizons.append(voyage_horizon)
        endpoint = self._get_endpoint(
            imo=imos,
            voyage_keys=voyage_keys,
            event_type=event_type,
            event_horizons=event_horizons,
            event_purpose=event_purposes,
            vessel_class_id=vessel_class_ids,
            port_ids=port_ids,
            vessel_type_id=vessel_type_id,
            start_date_from=start_date_from,
            start_date_to=start_date_to,
            first_load_arrival_date_from=first_load_arrival_date_from,
            first_load_arrival_date_to=first_load_arrival_date_to,
            end_date_from=end_date_from,
            end_date_to=end_date_to,
            market_info_rate_from=market_info_rate_from,
            market_info_rate_to=market_info_rate_to,
            market_info_rate_type=market_info_rate_type,
            commercial_operator_id=commercial_operator_id,
            charterer_id=charterer_id,
            voyage_horizon=voyage_horizons,
            token=token,
            hide_event_details=hide_event_details,
            hide_events=hide_events,
            hide_market_info=hide_market_info,
        )
        results, _ = self._get_voyages_pages(endpoint)
        return results

    def get_voyages_flat_by_advanced_search(
        self,
        imos: Optional[List[int]] = None,
        voyage_keys: Optional[List[str]] = None,
        event_type: Optional[int] = None,
        event_horizon: Optional[int] = None,
        event_horizons: Optional[List[int]] = None,
        event_purpose: Optional[str] = None,
        event_purposes: Optional[List[str]] = None,
        vessel_class_id: Optional[int] = None,
        vessel_class_ids: Optional[List[int]] = None,
        port_id: Optional[int] = None,
        port_ids: Optional[List[int]] = None,
        vessel_type_id: Optional[int] = None,
        start_date_from: Optional[date] = None,
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
        voyage_horizons: Optional[List[str]] = None,
        token: Optional[str] = None,
        hide_event_details: Optional[bool] = None,
        hide_events: Optional[bool] = None,
        hide_market_info: Optional[bool] = None,
    ) -> VoyagesFlat:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imos: If a list of imos is provided then only voyages of these
                imos will be returned
            voyage_keys: If provided only the voyages with the requested
                keys will be returned
            event_type: If an EventType is provided, then only voyages that
                include at least one event of this type will be returned.
            event_horizon: If an EventHorizon is provided, then only voyages
                of this event horizon will be returned.
            event_horizons: If a list of EventHorizons is provided then only
                voyages that include at least one event of those types
                will be returned
            event_purpose: If an EventPurpose is provided, then only voyages
                that include at least one event of this purpose will be
                returned.
            event_purposes: If a list of EventPurposes is provided then only
                voyages that include at least one event of this type
                will be returned
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, then voyages for all vessels are returned.
            vessel_class_ids: If provided only voyages of those vessel classes
                will be returned.
            port_id: If PortId is provided then only voyages that contains at
                least one event at this port will be returned.
            port_ids: If a list of ports is provided then only voyages that
                contains at least one event at those ports will be returned.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, then voyages for all vessels are returned.
            start_date_from: Return voyages after the provided voyage start
                date.
            start_date_to: Return voyages up to the provided voyage end date.
            first_load_arrival_date_from: Return voyages with a first load
                arrival date after the provided date.
            first_load_arrival_date_to: Return voyages with a first load
                arrival date up to the provided date.
            end_date_from: Return voyages with an end date after the provided
                date.
            end_date_to: Return voyages with an end date up to the provided
                date.
            market_info_rate_from: If provided, then only voyages that have
                market data and with rate greater than this will be returned.
            market_info_rate_to: If provided, then only voyages that have
                market data and with a lower rate will be returned.
            market_info_rate_type: If provided, then only voyages that have
                market data and with the same rate type will be returned.
            commercial_operator_id: If provided, then only voyages that have
                this commercial operator will be returned.
            charterer_id: If provided, then only voyages that have this
                charterer will be returned.
            voyage_horizon: If a VoyageHorizon is provided, then only voyages
                of that type will be returned.
            voyage_horizons: If a list of VoyageHorizon is provided then
                only voyages of that type will be returned.
            token: Token returned from the previous incremental call. If this
                is the first call, then it can be omitted.
            hide_event_details: If True, then event details will be excluded.
            hide_events: If True, then events will be excluded.
            hide_market_info: If True, then market information will be
                excluded.

        Returns:
            Voyages data in flat format as a tupple.
        """
        if event_horizon is not None:
            if event_horizons is None:
                event_horizons = []
            event_horizons.append(event_horizon)

        if event_purpose is not None:
            if event_purposes is None:
                event_purposes = []
            event_purposes.append(event_purpose)

        if vessel_class_id is not None:
            if vessel_class_ids is None:
                vessel_class_ids = []
            vessel_class_ids.append(vessel_class_id)

        if port_id is not None:
            if port_ids is None:
                port_ids = []
            port_ids.append(port_id)

        if voyage_horizon is not None:
            if voyage_horizons is None:
                voyage_horizons = []
            voyage_horizons.append(voyage_horizon)
        endpoint = self._get_endpoint(
            imo=imos,
            voyage_keys=voyage_keys,
            event_type=event_type,
            event_horizons=event_horizons,
            event_purpose=event_purposes,
            vessel_class_id=vessel_class_ids,
            port_ids=port_ids,
            vessel_type_id=vessel_type_id,
            voyage_date_from=start_date_from,
            voyage_date_to=start_date_to,
            start_date_from=start_date_from,
            start_date_to=start_date_to,
            first_load_arrival_date_from=first_load_arrival_date_from,
            first_load_arrival_date_to=first_load_arrival_date_to,
            end_date_from=end_date_from,
            end_date_to=end_date_to,
            market_info_rate_from=market_info_rate_from,
            market_info_rate_to=market_info_rate_to,
            market_info_rate_type=market_info_rate_type,
            commercial_operator_id=commercial_operator_id,
            charterer_id=charterer_id,
            voyage_horizon=voyage_horizons,
            token=token,
            hide_event_details=hide_event_details,
            hide_events=hide_events,
            hide_market_info=hide_market_info,
            nested=False
        )
        results, _ = self._get_voyages_flat_pages(endpoint)
        return results

    def get_voyages_condensed_by_advanced_search(
        self,
        imos: Optional[List[int]] = None,
        voyage_keys: Optional[List[str]] = None,
        event_type: Optional[int] = None,
        event_horizon: Optional[int] = None,
        event_horizons: Optional[List[int]] = None,
        event_purpose: Optional[str] = None,
        event_purposes: Optional[List[str]] = None,
        vessel_class_id: Optional[int] = None,
        vessel_class_ids: Optional[List[int]] = None,
        port_id: Optional[int] = None,
        port_ids: Optional[List[int]] = None,
        vessel_type_id: Optional[int] = None,
        start_date_from: Optional[date] = None,
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
        voyage_horizons: Optional[List[str]] = None,
        token: Optional[str] = None,
        hide_event_details: Optional[bool] = None,
        hide_events: Optional[bool] = None,
        hide_market_info: Optional[bool] = None,
    ) -> VoyagesCondensed:
        """Retrieves all voyages filtered with the provided parameters.

        Args:
            imos: If a list of imos is provided then only voyages of these
                imos will be returned
            voyage_keys: If provided only the voyages with the requested
                keys will be returned
            event_type: If an EventType is provided, then only voyages that
                include at least one event of this type will be returned.
            event_horizon: If an EventHorizon is provided, then only voyages
                of this event horizon will be returned.
            event_horizons: If a list of EventHorizons is provided then only
                voyages that include at least one event of those types
                will be returned
            event_purpose: If an EventPurpose is provided, then only voyages
                that include at least one event of this purpose will be
                returned.
            event_purposes: If a list of EventPurposes is provided then only
                voyages that include at least one event of this type
                will be returned
            vessel_class_id: Return only voyages for the provided vessel
                class. If None, then voyages for all vessels are returned.
            vessel_class_ids: If provided only voyages of those vessel classes
                will be returned.
            port_id: If PortId is provided then only voyages that contains at
                least one event at this port will be returned.
            port_ids: If a list of ports is provided then only voyages that
                contains at least one event at those ports will be returned.
            vessel_type_id: Return only voyages for the provided vessel type.
                If None, then voyages for all vessels are returned.
            start_date_from: Return voyages after the provided voyage start
                date.
            start_date_to: Return voyages up to the provided voyage end date.
            first_load_arrival_date_from: Return voyages with a first load
                arrival date after the provided date.
            first_load_arrival_date_to: Return voyages with a first load
                arrival date up to the provided date.
            end_date_from: Return voyages with an end date after the provided
                date.
            end_date_to: Return voyages with an end date up to the provided
                date.
            market_info_rate_from: If provided, then only voyages that have
                market data and with rate greater than this will be returned.
            market_info_rate_to: If provided, then only voyages that have
                market data and with a lower rate will be returned.
            market_info_rate_type: If provided, then only voyages that have
                market data and with the same rate type will be returned.
            commercial_operator_id: If provided, then only voyages that have
                this commercial operator will be returned.
            charterer_id: If provided, then only voyages that have this
                charterer will be returned.
            voyage_horizon: If a VoyageHorizon is provided, then only voyages
                of that type will be returned.
            voyage_horizons: If a list of VoyageHorizon is provided then
                only voyages of that type will be returned.
            token: Token returned from the previous incremental call. If this
                is the first call, then it can be omitted.
            hide_event_details: If True, then event details will be excluded.
            hide_events: If True, then events will be excluded.
            hide_market_info: If True, then market information will be
                excluded.

        Returns:
            Voyages data in condensed format as a tupple.
        """
        if event_horizon is not None:
            if event_horizons is None:
                event_horizons = []
            event_horizons.append(event_horizon)

        if event_purpose is not None:
            if event_purposes is None:
                event_purposes = []
            event_purposes.append(event_purpose)

        if vessel_class_id is not None:
            if vessel_class_ids is None:
                vessel_class_ids = []
            vessel_class_ids.append(vessel_class_id)

        if port_id is not None:
            if port_ids is None:
                port_ids = []
            port_ids.append(port_id)

        if voyage_horizon is not None:
            if voyage_horizons is None:
                voyage_horizons = []
            voyage_horizons.append(voyage_horizon)
        endpoint = self._get_endpoint(
            imo=imos,
            voyage_keys=voyage_keys,
            event_type=event_type,
            event_horizons=event_horizons,
            event_purpose=event_purposes,
            vessel_class_id=vessel_class_ids,
            port_ids=port_ids,
            vessel_type_id=vessel_type_id,
            voyage_date_from=start_date_from,
            voyage_date_to=start_date_to,
            start_date_from=start_date_from,
            start_date_to=start_date_to,
            first_load_arrival_date_from=first_load_arrival_date_from,
            first_load_arrival_date_to=first_load_arrival_date_to,
            end_date_from=end_date_from,
            end_date_to=end_date_to,
            market_info_rate_from=market_info_rate_from,
            market_info_rate_to=market_info_rate_to,
            market_info_rate_type=market_info_rate_type,
            commercial_operator_id=commercial_operator_id,
            charterer_id=charterer_id,
            voyage_horizon=voyage_horizons,
            token=token,
            hide_event_details=hide_event_details,
            hide_events=hide_events,
            hide_market_info=hide_market_info,
            nested=False,
            condensed=True
        )
        results, _ = self._get_voyages_condensed_pages(endpoint)
        return results

    def get_vessel_classes(
        self, class_filter: Optional[VesselClassFilter] = None
    ) -> Tuple[VesselClass, ...]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If
                not specified, returns all available vessel classes.

        Returns:
            A tuple of available vessel classes that match the filter.
        """
        response = self.__connection._make_get_request(
            "voyages-api/v4/filters/availableVesselClasses"
        )
        response.raise_for_status()

        classes = (parse_model(c, VesselClass) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))

    def get_vessel_types(
        self, type_filter: Optional[VesselTypeFilter] = None
    ) -> Tuple[VesselType, ...]:
        """Retrieves available vessel types.

        Args:
            type_filter: A filter used to find specific vessel types. If not
                specified, returns all available vessel types.

        Returns:
            A tuple of available vessel types that match the filter.
        """
        response = self.__connection._make_get_request(
            "voyages-api/v4/filters/availableVesselTypes"
        )
        response.raise_for_status()

        types = (parse_model(c, VesselType) for c in response.json())
        type_filter = type_filter or VesselTypeFilter()

        return tuple(type_filter._apply(types))

    def get_imos(
        self, vessel_filter: Optional[VesselFilter] = None
    ) -> Tuple[Vessel, ...]:
        """Retrieves available vessel types.

        Args:
            vessel_filter: A filter used to find specific vessel . If not
                specified, returns all available vessels .

        Returns:
            A tuple of available vessels that match the filter.
        """
        response = self.__connection._make_get_request(
            "voyages-api/v4/filters/availableVessels"
        )
        response.raise_for_status()

        vessels = (parse_model(c, Vessel) for c in response.json())
        vessel_filter = vessel_filter or VesselFilter()

        return tuple(vessel_filter._apply(vessels))
