# noqa: D100

from datetime import date, time
from typing import Optional

from .. import Connection, Port, VesselClass
from .._internals import format_iso_date, QueryString
from .historical_tonnage_list import HistoricalTonnageList
from .vessel_filter import VesselFilter
from . import _historical_tonnage_list_json


class HistoricalTonnageListAPI:
    """Represents Signal's Historical Tonnage List API."""

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
            vessel_class: The class of vessels to return.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                after the end date.
            start_date: The date of the earliest tonnage list in the response.
            end_date: The date of the latest tonnage list in the response.
            time: Specifies the time of day for which the state of the tonnage
                lists will be retrieved.
            vessel_filter: A filter defining which vessels should be included
                in the response.

        Returns:
            Given a time-range, returns a Historical Tonnage List containing a
            Tonnage List for every day between the start and end dates, at the
            requested time of day.
        """
        query_string: QueryString = {
            "loadingPort": loading_port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": laycan_end_in_days,
            "startDate": format_iso_date(start_date),
            "endDate": format_iso_date(end_date),
            "time": time.strftime("%H:%M") if time else None,
            **(vessel_filter._to_query_string() if vessel_filter else {}),
        }

        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/", query_string
        )

        response.raise_for_status()
        return _historical_tonnage_list_json.parse(response.json())
