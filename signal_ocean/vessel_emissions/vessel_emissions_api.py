"""The vessel emissions api."""
import os
import copy
from typing import Optional, List, Union, Dict, Any
from urllib.parse import urljoin, urlencode
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_multiple, get_single
from signal_ocean.vessel_emissions.models import EmissionsEstimation, \
    VesselMetrics, VesselClassEmissions, VesselClassMetrics


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


class VesselEmissionsAPI:
    """Represents Signal's Vessel Emissions API."""

    relative_url = "vessel-emissions-api/public/v2/"
    default_pit = str(date.today())

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VesselEmissionsAPI.

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

    def construct_url_parameters(
            self,
            quantity: Union[int, None] = None,
            token: Optional[str] = None,
            include_consumptions: bool = False,
            include_efficiency_metrics: bool = False,
            include_distances: bool = False,
            include_durations: bool = False,
            include_speed_statistics: bool = False,
            include_eu_emissions: bool = False,
            sulphur_content_hfo: Optional[Union[float, None]] = None,
            sulphur_content_lfo: Optional[Union[float, None]] = None,
            sulphur_content_mgo: Optional[Union[float, None]] = None,
            sulphur_content_lng: Optional[Union[float, None]] = None
    ) -> Dict[Any, str]:
        """Construct the request parameters based on the user's input.

        Args:
        quantity: Cargo quantity of the voyage
        token: Next page token
        include_consumptions: Include consumption data in response
        include_efficiency_metrics: Include efficiency metrics in response
        include_distances: Include distances data in the response
        include_durations: Include duration data in the response
        include_speed_statistics: Include speed statistics data in response
        include_eu_emissions: Include European Union related
        emissions in response
        sulphur_content_hfo: Sulphur Content of HFO fuel type
        sulphur_content_lfo: Sulphur Content of LFO fuel type
        sulphur_content_mgo: Sulphur Content of MGO fuel type
        sulphur_content_lng: Sulphur Content of LNG fuel type

        Returns:
            The parameters dictionary of Request URL
        """
        params = {}
        if quantity is not None:
            params['quantity'] = str(quantity)
        if token is not None:
            params['token'] = token
        params['include_consumptions'] = str(include_consumptions)
        params['include_efficiency_metrics'] = str(include_efficiency_metrics)
        params['include_distances'] = str(include_distances)
        params['include_durations'] = str(include_durations)
        params['include_speed_statistics'] = str(include_speed_statistics)
        params['include_eu_emissions'] = str(include_eu_emissions)
        if sulphur_content_hfo is not None:
            params['sulphur_content_hfo'] = str(sulphur_content_hfo)
        if sulphur_content_lfo is not None:
            params['sulphur_content_lfo'] = str(sulphur_content_lfo)
        if sulphur_content_mgo is not None:
            params['sulphur_content_mgo'] = str(sulphur_content_mgo)
        if sulphur_content_lng is not None:
            params['sulphur_content_lng'] = str(sulphur_content_lng)
        return params

    def get_emissions_by_imo_and_voyage_number(
            self,
            imo: int,
            voyage_number: int,
            quantity: Union[int, None] = None,
            include_consumptions: bool = False,
            include_efficiency_metrics: bool = False,
            include_distances: bool = False,
            include_durations: bool = False,
            include_speed_statistics: bool = False,
            include_eu_emissions: bool = False,
            sulphur_content_hfo: Union[float, None] = None,
            sulphur_content_lfo: Union[float, None] = None,
            sulphur_content_mgo: Union[float, None] = None,
            sulphur_content_lng: Union[float, None] = None
    ) -> Optional[EmissionsEstimation]:
        """Retrieves voyage emissions for a vessel by its IMO and Voyage Number.

        Args:
            imo: Vessel IMO to retrieve.
            voyage_number: Voyage Number to retrieve.
            quantity: User defined transported quantity for voyage.
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics in response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics in response.
            include_eu_emissions: Include European Union related
            emissions in response.
            sulphur_content_hfo: Sulphur Content of HFO fuel type.
            sulphur_content_lfo: Sulphur Content of LFO fuel type.
            sulphur_content_mgo: Sulphur Content of MGO fuel type.
            sulphur_content_lng: Sulphur Content of LNG fuel type.

        Returns:
            EmissionsEstimation if no vessel with
            the specified IMO or Voyage Number has been found.
        """
        params_dict = self.construct_url_parameters(
            quantity=quantity,
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_speed_statistics=include_speed_statistics,
            include_eu_emissions=include_eu_emissions,
            sulphur_content_hfo=sulphur_content_hfo,
            sulphur_content_lfo=sulphur_content_lfo,
            sulphur_content_mgo=sulphur_content_mgo,
            sulphur_content_lng=sulphur_content_lng)
        query_url = make_url('emissions',
                             'imo', imo,
                             'voyage_number', voyage_number,
                             **params_dict)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, EmissionsEstimation)

    def get_emissions_by_imo(
            self,
            imo: int,
            include_consumptions: bool = False,
            include_efficiency_metrics: bool = False,
            include_distances: bool = False,
            include_durations: bool = False,
            include_speed_statistics: bool = False,
            include_eu_emissions: bool = False,
            sulphur_content_hfo: Union[float, None] = None,
            sulphur_content_lfo: Union[float, None] = None,
            sulphur_content_mgo: Union[float, None] = None,
            sulphur_content_lng: Union[float, None] = None
    ) -> List[EmissionsEstimation]:
        """Retrieves a list of vessel emissions by its IMO.

        Args:
            imo: IMO of the vessel to retrieve emissions.
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics
             data in the response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics
             data in the response.
            include_eu_emissions: Include European Union related
             emissions data in the response.
            sulphur_content_hfo: Sulphur Content of HFO fuel type.
            sulphur_content_lfo: Sulphur Content of LFO fuel type.
            sulphur_content_mgo: Sulphur Content of MGO fuel type.
            sulphur_content_lng: Sulphur Content of LNG fuel type.

        Returns:
            A list of vessel emissions or None if no vessel
             with the specified IMO has been found.
        """
        params_dict = self.construct_url_parameters(
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_speed_statistics=include_speed_statistics,
            include_eu_emissions=include_eu_emissions,
            sulphur_content_hfo=sulphur_content_hfo,
            sulphur_content_lfo=sulphur_content_lfo,
            sulphur_content_mgo=sulphur_content_mgo,
            sulphur_content_lng=sulphur_content_lng
        )
        query_url = make_url('emissions',
                             'imo', imo,
                             **params_dict)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return [i for i in get_multiple(self.__connection,
                                        url,
                                        EmissionsEstimation)]

    def get_metrics_by_imo(
            self,
            imo: int,
            year: Union[int, None] = None
    ) -> List[VesselMetrics]:
        """Get vessel metrics.

        Args:
            imo: Vessel IMO to retrieve
            year: The year for the annual metrics

        Returns:
            VesselMetrics for the requested IMO

        """
        url = urljoin(VesselEmissionsAPI.relative_url,
                      f"emissions/metrics/imo/{imo}")
        if year is not None:
            url = urljoin(url, f"?year={year}")
        return [i for i in get_multiple(self.__connection,
                                        url,
                                        VesselMetrics)]

    def get_emissions_by_vessel_class_id(
            self,
            vessel_class_id: int,
            token: Union[str, None] = None,
            include_consumptions: bool = False,
            include_efficiency_metrics: bool = False,
            include_distances: bool = False,
            include_durations: bool = False,
            include_speed_statistics: bool = False,
            include_eu_emissions: bool = False
    ) -> Optional[VesselClassEmissions]:
        """Get emissions estimations for a vessel class (supports incremental updates).

        Args:
            vessel_class_id: The vessel class to retrieve
            token: Next page token
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics
             data in the response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics
             data in the response.
            include_eu_emissions: Include European Union related emissions
             data in the response.

        Returns:
            List of emissions estimation for all
             available voyages of a vessel class.

        """
        params_dict = self.construct_url_parameters(
            token=token,
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_speed_statistics=include_speed_statistics,
            include_eu_emissions=include_eu_emissions
        )
        query_url = make_url('emissions',
                             'class', vessel_class_id,
                             **params_dict)

        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection,
                          url,
                          VesselClassEmissions)

    def get_metrics_by_vessel_class_id(self,
                                       vessel_class_id: int,
                                       year: Union[int, None] = None,
                                       token: Union[str, None] = None
                                       ) -> Optional[VesselClassMetrics]:
        """Get vessel class metrics.

        Args:
            vessel_class_id: The vessel class to retrieve
            year: The year for the annual metrics
            token: Next page token

        Returns:
            VesselClassMetrics for the requested Class

        """
        if year is None and token is None:
            query_url = ""
        else:
            query_url = "?"
            if year is not None:
                query_url += f"year={year}"
                if token is not None:
                    query_url += f"&token={token}"
            else:
                if token is not None:
                    query_url += f"token={token}"
        query_url = urljoin(f"emissions/metrics/class/"
                            f"{vessel_class_id}",
                            query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, VesselClassMetrics)
