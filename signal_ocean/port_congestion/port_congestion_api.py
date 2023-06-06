"""Signal's Port Congestion API Wrapper."""
from datetime import date
from typing import List, Optional


from signal_ocean import Connection
from signal_ocean.port_congestion.models import (
    PortCongestionQueryResponse,
    PortCongestionTimeSeriesEntry,
)
from signal_ocean.util.request_helpers import get_single


class PortCongestionAPI:
    """Signal's Port Congestion API Wrapper."""

    base_url = "port-congestion-api"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes PortCongestionAPI.

        Args:
            connection (Connection, optional): API connection configuration.
                                               If not provided, the default
                                               connection method is used.
        """
        self.__connection = connection or Connection()

    def query_port_congestion(
        self,
        ports: Optional[List[str]] = None,
        port_ids: Optional[List[int]] = None,
        level_0_areas: Optional[List[str]] = None,
        level_0_area_ids: Optional[List[int]] = None,
        level_1_areas: Optional[List[str]] = None,
        level_1_area_ids: Optional[List[int]] = None,
        countries: Optional[List[str]] = None,
        country_ids: Optional[List[int]] = None,
        vessel_types: Optional[List[str]] = None,
        vessel_type_ids: Optional[List[int]] = None,
        vessel_classes: Optional[List[str]] = None,
        vessel_class_ids: Optional[List[int]] = None,
        date_from: Optional[date] = None,
    ) -> Optional[List[PortCongestionTimeSeriesEntry]]:
        """Exposes Port Congestion's `query` endpoint.

        Args:
            ports (list, optional): A list of Port Names. Defaults to None.
            port_ids (list, optional): A list of Port IDs. Defaults to None.
            level_0_areas (list, optional): A list of Level 0 Area names.
                                            Defaults to None.
            level_0_area_ids (list, optional): A list of Level 0 Area IDs.
                                               Defaults to None.
            level_1_areas (list, optional): A list of Level 1 Area names.
                                            Defaults to None.
            level_1_area_ids (list, optional): A list of Level 1 Area IDs.
                                               Defaults to None.
            countries (list, optional): A list of Country names.
                                        Defaults to None.
            country_ids (list, optional): A list of Country IDs.
                                          Defaults to None.
            vessel_types (list, optional): A list of Vessel Type names.
                                           Defaults to None.
            vessel_type_ids (list, optional): A list of Vessel Type IDs.
                                              Defaults to None.
            vessel_classes (list, optional): A list of Vessel Class names.
                                             Defaults to None.
            vessel_class_ids (list, optional): A list of Vessel Class IDs.
                                               Defaults to None.
            date_from (date, optional): A Date point to query from.
                                        Defaults to None.

        Raises:
            RuntimeError: In case of any request issue.

        Returns:
            List[PortCongestionTimeSeriesEntry], optional:
                A list of PortCongestionTimeSeriesEntry or None.
        """
        query_url = f"{self.base_url}/api/v1/query/"
        params = {
            "Ports": ports,
            "PortIDs": port_ids,
            "Level0Areas": level_0_areas,
            "Level0AreasIDs": level_0_area_ids,
            "Level1Areas": level_1_areas,
            "Level1AreaIDs": level_1_area_ids,
            "Countries": countries,
            "CountriesIDs": country_ids,
            "VesselTypes": vessel_types,
            "VesselTypeIDs": vessel_type_ids,
            "VesselClasses": vessel_classes,
            "VesselClassIDs": vessel_class_ids,
            "DateFrom": date_from.isoformat() if date_from else None,
        }

        response = get_single(
            connection=self.__connection,
            relative_url=query_url,
            cls=PortCongestionQueryResponse,
            query_string=params,
        )

        if not response:
            return None

        if response.query_errors is not None:
            raise RuntimeError(
                f"Port Congestion API errors occurred:"
                f"\n{[error for error in response.query_errors]}"
            )

        return response.time_series
