# noqa: D100

from datetime import date, time, timedelta
from typing import Optional, Iterable, List

from .. import Connection, Port, VesselClass
from .._internals import format_iso_date, QueryString
from .historical_tonnage_list import HistoricalTonnageList
from .tonnage_list import TonnageList
from .vessel_filter import VesselFilter
from . import _historical_tonnage_list_json


class _DateRange:
    def __init__(self, start: Optional[date], end: Optional[date]):
        if start is not None and end is not None and end < start:
            raise ValueError("Start date cannot be after end date.")

        self.start = start
        self.end = end

    def split(self, max_days: int) -> Iterable["_DateRange"]:
        if max_days < 1:
            raise ValueError(
                f"Date range cannot be split into chunks of {max_days} days."
            )

        max_size = timedelta(days=max_days - 1)
        current_start = self.start

        if current_start is not None and self.end is not None:
            while self.end - current_start > max_size:
                current_end = current_start + max_size
                yield _DateRange(current_start, current_end)
                current_start = current_end + timedelta(days=1)

        yield _DateRange(current_start, self.end)


class HistoricalTonnageListAPI:
    """Handles communications with  Signal's Historical Tonnage List API."""

    __MAX_DATE_RANGE_DAYS = 365

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes HistoricalTonnageListAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_historical_tonnage_list(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        laycan_end_in_days: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        time: Optional[time] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> HistoricalTonnageList:
        """Retrieves a Historical Tonnage List.

        If no input dates are provided, the last 10 days will be fetched
        (including today).

        To get a tonnage list for a specific day, set both date parameters to
        the desired date.

        Args:
            loading_port: The loading port from which ETA will be calculated.
            vessel_class: The vessel class to calculate the tonnage lists.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                after the end date.
            start_date: The date of the earliest tonnage list in the response.
            end_date: The date of the latest tonnage list in the response.
            time: Specifies the UTC time of day for which the state of
                the tonnage lists will be retrieved.
                It can get the values 00, 06, 12, 18.
            vessel_filter: A filter defining which vessels should be included
                in the response see Vessel Filter class for more details.

        Returns:
            Given a time-range, returns a Historical Tonnage List containing a
            Tonnage List for every day between the start and end dates, at the
            requested time of day.
        """
        all_tonnage_lists: List[TonnageList] = []
        date_ranges = _DateRange(start_date, end_date).split(
            HistoricalTonnageListAPI.__MAX_DATE_RANGE_DAYS
        )

        for date_range in date_ranges:
            tonnage_lists = self._get_htl_chunk(
                loading_port,
                vessel_class,
                date_range,
                laycan_end_in_days,
                time,
                vessel_filter,
            )
            all_tonnage_lists.extend(tonnage_lists)

        return HistoricalTonnageList(all_tonnage_lists)

    def _get_htl_chunk(
        self,
        loading_port: Port,
        vessel_class: VesselClass,
        date_range: _DateRange,
        laycan_end_in_days: Optional[int] = None,
        time: Optional[time] = None,
        vessel_filter: Optional[VesselFilter] = None,
    ) -> Iterable[TonnageList]:
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            "startDate": format_iso_date(date_range.start),
            "endDate": format_iso_date(date_range.end),
            "time": time.strftime("%H:%M") if time else None,
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/", query_string
        )

        response.raise_for_status()
        return _historical_tonnage_list_json.parse_tonnage_lists(
            response.json()
        )
