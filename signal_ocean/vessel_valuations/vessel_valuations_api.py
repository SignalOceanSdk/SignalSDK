"""The vessel valuations api."""
import copy
import os
from typing import Optional, Dict, Union, List
from urllib.parse import urlencode

from signal_ocean.connection import Connection
from signal_ocean.util.request_helpers \
    import get_multiple, get_single, post_multiple
from signal_ocean.vessel_valuations.models \
    import (Valuation, HistoricalValuation, PageValuations)


def make_url(
        base_url: str,
        *res: Union[str, int],
        **params: str
) -> str:
    """Constructs url for the request.

    Args:
        base_url: the base to build the url.
        Can be either emissions or emissions/metrics

    """
    url = base_url
    for r in res:
        url = '{}/{}'.format(url, r)
    if params:
        url = '{}?{}'.format(url, urlencode(params))
    return url


def custom_headers(connection: Connection) -> Dict[str, Optional[str]]:
    """Custom function to change the request header.

    Args:
        connection: Connection object

    Returns:
        headers dict

    """
    return {
        "Ocp-Apim-Subscription-Key":
            connection._Connection__api_key  # type: ignore
            or os.environ.get("SIGNAL_OCEAN_API_KEY"),
        "Content-Type": "application/json",
        "Source": "SignalSDK",
    }


class VesselValuationsAPI:
    """Represents Signal's Vessel Valuation API."""

    relative_url = "valuationsv2/api/v2/valuations"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes Vessels Valuations API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        if connection is not None:
            em_connection = copy.deepcopy(connection)
            func_type = type(
                em_connection._Connection__get_headers  # type: ignore
            )
            em_connection._Connection__get_headers = func_type(  # type: ignore
                custom_headers, em_connection
            )
            self.__connection = em_connection
        else:
            connection = Connection()
            func_type = type(
                connection._Connection__get_headers  # type: ignore
            )
            connection._Connection__get_headers = func_type(  # type: ignore
                custom_headers, connection
            )
            self.__connection = connection

    def get_all_historical_valuations_by_imo(
            self,
            imo: int,
            from_date: Optional[str] = None,
            to_date: Optional[str] = None,
    ) -> Optional[List[HistoricalValuation]]:
        """Retrieves the latest valuation price (in $M) for a specific vessel.

        Args:
            imo: The IMO number of the vessel.
            from_date: The first date of valuation (optional).
            to_date: The last date of valuation (optional).

        Returns:
            A List of Historical Valuations for this vessel.
        """
        params_dict = {}
        if from_date is not None:
            params_dict['FromDate'] = from_date
        if to_date is not None:
            params_dict['ToDate'] = to_date
        query_url = make_url(VesselValuationsAPI.relative_url,
                             imo,
                             'historical',
                             **params_dict)
        historical_valuations = [
            i for i in get_multiple(
                self.__connection,
                query_url,
                HistoricalValuation
            )
        ]
        return historical_valuations

    def get_latest_valuation_by_imo(self, imo: int) -> Optional[Valuation]:
        """Retrieves the latest valuation for a specific vessel.

        Args:
            imo: The IMO number of the vessel.

        Returns:
            A valuation or None if a vessel with the given IMO number does not
            exist or has no valuation.
        """
        url = make_url(VesselValuationsAPI.relative_url,
                       imo,
                       'latest')
        valuation = get_single(self.__connection, url, Valuation)
        return valuation

    def get_latest_valuations_by_page(self,
                                      page: Optional[int] = None,
                                      page_size: Optional[int] = None,
                                      changed_since: Optional[str] = None
                                      ) -> Optional[PageValuations]:
        """Retrieves all valuations for a specific vessel.

        Args:
            page:  The page number you are requesting.
            page_size:  The maximum number of results per
            page to be returned.
            Range between 1 and 500, by default 100.
            changed_since: The date since the
            last time of update (optional).

        Returns:
            A tuple of valuations or None if a vessel with the given IMO number
            does not exist.
        """
        params_dict = {}
        if page is not None:
            params_dict['Page'] = str(page)
        if page_size is not None:
            params_dict['PageSize'] = str(page_size)
        if changed_since is not None:
            params_dict['ChangedSince'] = str(changed_since)
        url = make_url(VesselValuationsAPI.relative_url,
                       'latest',
                       '',
                       **params_dict)
        return get_single(self.__connection, url, PageValuations)

    def get_latest_valuations_for_list_of_vessels(
            self,
            imo_list: List[int]
    ) -> List[Optional[Valuation]]:
        """Retrieves the latest estimated valuations for a list of vessels.

        Args:
            imo_list: The list of IMO numbers of the vessels.

        Returns:
            A list of latest valuations
            for the requested imo numbers.
        """
        data = post_multiple(
            connection=self.__connection,
            relative_url=f"{VesselValuationsAPI.relative_url}/latest",
            cls=Valuation,
            query_string=imo_list  # type: ignore
        )
        return [i for i in data]
