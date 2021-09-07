from datetime import date
from typing import Optional, Tuple, List
from urllib.parse import urljoin, urlencode

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single, get_multiple
from signal_ocean.util.parsing_helpers import _to_camel_case
from signal_ocean.oilx_cargo_tracking.oilx_models import CargoFlow, CargoFlowsPagedResponse

CargoFlows = Tuple[CargoFlow, ...]
NextRequestToken = str

class OilxCargoTrackingAPI:

    relative_url = "oilx-cargo-tracking-api/v1/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VoyagesAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    @staticmethod
    def _get_endpoint(vessel_class_id: Optional[int] = None,
                      incremental: bool = False) -> str:

        endpoint = 'cargoTracking'
       
        if vessel_class_id is not None:
            endpoint += f'/class/{vessel_class_id}'
        if incremental:
            endpoint += f'/incremental'

        return urljoin(OilxCargoTrackingAPI.relative_url, endpoint)

    def _get_oilx_cargoes_pages(
        self, endpoint: str, token: Optional[str] = None
        ) -> Tuple[CargoFlows, Optional[NextRequestToken]]:
   
            results: List[CargoFlow] = []
            next_page_token = token
            while True:
                params = {'token': next_page_token} \
                    if next_page_token is not None else None
                response = get_single(self.__connection, endpoint,
                                    CargoFlowsPagedResponse, query_string=params)
                if response is not None and response.data is not None:
                    results.extend(response.data)
                next_page_token = response.next_page_token \
                    if response is not None else None

                if next_page_token is None:
                    break

            next_request_token = response.next_request_token \
                if response is not None else None
            return tuple(results), next_request_token        

    def get_oilx_cargoes(
        self,
        vessel_class_id: Optional[int] = None
        ) -> CargoFlows:

       endpoint = self._get_endpoint(vessel_class_id, incremental=False) 
    
       results, _ = self._get_oilx_cargoes_pages(endpoint)
        
       return results
       
