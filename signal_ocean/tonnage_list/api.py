# noqa: D100

from typing import Optional

from .. import Connection
from ..historical_tonnage_list import VesselFilter
from .. import Port, VesselClass
from .models import TonnageList
from . import _tonnage_list_json
from .._internals import QueryString


class TonnageListAPI:
    """Handles communication with Signal's Tonnage List API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes TonnageListAPI.

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
            loading_port: The loading port from which ETA will be calculated.
            vessel_class: Vessel class of vessels in the tonnage list.
            laycan_end_in_days: The maximum ETA expressed as a number of days
                from now.
            vessel_filter: A filter defining which vessels should be included
                in the response. See the VesselFilter class for more details.

        Returns:
            Returns a tonnage list containing vessels that match the specified
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
        return _tonnage_list_json.parse_tonnage_list(response.json())
