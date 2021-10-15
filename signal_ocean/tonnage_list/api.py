"""Tonnage List API."""

from typing import Optional, Tuple

from .. import Connection
from .models import (
    DateRange,
    HistoricalTonnageList,
    Port,
    PortFilter,
    TonnageList,
    VesselClass,
    VesselClassFilter,
    VesselFilter,
)
from . import _json
from .._internals import QueryString


class TonnageListAPI:
    """Handles communication with Signal's Tonnage List API."""

    __MAX_DATE_RANGE_DAYS = 365

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes `TonnageListAPI`.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_tonnage_list(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        laycan_end_in_days: Optional[int] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> TonnageList:
        """Retrieves a tonnage list.

        Args:
            loading_port: A loading port from which ETA will be calculated.
            vessel_class: The vessel class of vessels in the tonnage list.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                from now.
            vessel_filter: A filter defining which vessels should be included
                in the response. See the `VesselFilter` class for details.

        Returns:
            Returns a `TonnageList` containing vessels that match the specified
            criteria.
        """
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/tonnage-list/", query_string
        )

        response.raise_for_status()
        return _json.parse_tonnage_list_response(response.json())

    def get_historical_tonnage_list(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        laycan_end_in_days: Optional[int] = None,
        date_range: Optional[DateRange] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> HistoricalTonnageList:
        """Retrieves a historical tonnage list.

        If no input dates are provided, the last 10 days will be fetched
        (including today).

        To get a tonnage list for a specific day, set both date parameters to
        the desired date.

        Args:
            loading_port: A loading port from which ETA will be calculated.
            vessel_class: The vessel class of vessels in the tonnage list.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                after the end date.
            date_range: A range of dates for which to get historical tonnage
                lists.
            vessel_filter: A filter defining which vessels should be included
                in the response. See `VesselFilter` class for details.

        Returns:
            Given a time-range, returns a `HistoricalTonnageList` containing a
            `TonnageList` for every day between the start and end dates.
        """
        date_ranges = (date_range or DateRange(start=None, end=None))._split(
            TonnageListAPI.__MAX_DATE_RANGE_DAYS
        )

        tonnage_lists = (
            tonnage_list
            for dr in date_ranges
            for tonnage_list in self._get_htl_chunk(
                loading_port,
                vessel_class,
                dr,
                laycan_end_in_days,
                vessel_filter,
            )
        )

        return HistoricalTonnageList(tonnage_lists)

    def _get_htl_chunk(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        date_range: DateRange,
        laycan_end_in_days: Optional[int] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> HistoricalTonnageList:
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            **date_range._to_query_string(),
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/", query_string
        )

        response.raise_for_status()
        return _json.parse_historical_tonnage_list_response(response.json())

    def get_ports(
        self, port_filter: Optional[PortFilter] = None
    ) -> Tuple[Port, ...]:
        """Retrieves available ports.

        Args:
            port_filter: A filter used to find specific ports. If not
                specified, returns all available ports.

        Returns:
            A tuple of available ports that match the filter.
        """
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

    def get_vessel_classes(
        self, class_filter: Optional[VesselClassFilter] = None
    ) -> Tuple[VesselClass, ...]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If not
                specified, returns all available vessel classes.

        Returns:
            A tuple of available vessel classes that match the filter.
        """
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/vessel-classes"
        )
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))
