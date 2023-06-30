"""The vessel emissions api."""
from typing import Optional, List, Union
from urllib.parse import urljoin
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_multiple, get_single
from signal_ocean.vessel_emissions.models import EmissionsEstimation, VesselMetrics, VesselClassEmissions, \
    VesselClassMetrics


class VesselEmissionsAPI:
    """Represents Signal's Vessel Emissions API."""

    relative_url = "vessel-emissions-api/public/v2/"
    default_pit = str(date.today())

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VesselsAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def construct_emissions_url_parameters(self,
                                           quantity: Union[int, None] = None,
                                           token: Union[str, None] = None,
                                           include_consumptions: bool = False,
                                           include_efficiency_metrics: bool = False,
                                           include_distances: bool = False,
                                           include_durations: bool = False,
                                           include_speed_statistics: bool = False,
                                           include_eu_emissions: bool = False,
                                           sulphur_content_hfo: Union[float, None] = 0.025,
                                           sulphur_content_lfo: Union[float, None] = 0.001,
                                           sulphur_content_mgo: Union[float, None] = 0.001,
                                           sulphur_content_lng: Union[float, None] = 0.00004
                                           ) -> str:
        """Construct the request URL based on the input parameters.

        Args:
            quantity: Cargo quantity of the voyage
            token: Next page token
            include_consumptions: Include consumption data in the response
            include_efficiency_metrics: Include efficiency metrics data in the response
            include_distances: Include distances data in the response
            include_durations: Include duration data in the response
            include_speed_statistics: Include speed statistics data in the response
            include_eu_emissions: Include European Union related emissions data in the response
            sulphur_content_hfo: Sulphur Content of HFO fuel type
            sulphur_content_lfo: Sulphur Content of LFO fuel type
            sulphur_content_mgo: Sulphur Content of MGO fuel type
            sulphur_content_lng: Sulphur Content of LNG fuel type

        Returns:
            The last part of Request URL
        """
        url = "?"
        if quantity:
            url = urljoin(url, f"quality={quantity}")
        if token:
            url = urljoin(url, f"token={token}")
        query_url = f"include_consumptions={include_consumptions}&include_efficiency_metrics={include_efficiency_metrics}&include_distances={include_distances}" \
                    f"&include_durations={include_durations}&include_speed_statistics={include_speed_statistics}&include_eu_emissions={include_eu_emissions}"
        url = urljoin(url, query_url)
        if sulphur_content_hfo:
            url = urljoin(url, f"&sulphur_content_hfo={sulphur_content_hfo}")
        if sulphur_content_lfo:
            url = urljoin(url, f"&sulphur_content_lfo={sulphur_content_lfo}")
        if sulphur_content_mgo:
            url = urljoin(url, f"&sulphur_content_mgo={sulphur_content_mgo}")
        if sulphur_content_lng:
            url = urljoin(url, f"&sulphur_content_lng={sulphur_content_lng}")
        return url

    def get_emissions_by_imo_and_voyage_number(self,
                                               imo: int,
                                               voyage_number: int,
                                               quantity: Union[int, None] = None,
                                               include_consumptions: bool = False,
                                               include_efficiency_metrics: bool = False,
                                               include_distances: bool = False,
                                               include_durations: bool = False,
                                               include_speed_statistics: bool = False,
                                               include_eu_emissions: bool = False,
                                               sulphur_content_hfo: Union[float, None] = 0.025,
                                               sulphur_content_lfo: Union[float, None] = 0.001,
                                               sulphur_content_mgo: Union[float, None] = 0.001,
                                               sulphur_content_lng: Union[float, None] = 0.00004
                                               ) -> Optional[EmissionsEstimation]:
        """Retrieves voyage emissions for a vessel by its IMO and Voyage Number.

        Args:
            imo: Vessel IMO to retrieve.
            voyage_number: Voyage Number to retrieve.
            quantity: User defined transported quantity for voyage.
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics data in the response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics data in the response.
            include_eu_emissions: Include European Union related emissions data in the response.
            sulphur_content_hfo: Sulphur Content of HFO fuel type.
            sulphur_content_lfo: Sulphur Content of LFO fuel type.
            sulphur_content_mgo: Sulphur Content of MGO fuel type.
            sulphur_content_lng: Sulphur Content of LNG fuel type.

        Returns:
            EmissionsEstimation if no vessel with the specified IMO or Voyage Number has
                been found.
        """
        query_url = self.construct_emissions_url_parameters(quantity=quantity,
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
        query_url = urljoin(f"emissions/imo/{imo}/voyage_number/{voyage_number}", query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, EmissionsEstimation)

    def get_emissions_by_imo(self, imo: int,
                             include_consumptions: bool = False,
                             include_efficiency_metrics: bool = False,
                             include_distances: bool = False,
                             include_durations: bool = False,
                             include_speed_statistics: bool = False,
                             include_eu_emissions: bool = False,
                             sulphur_content_hfo: Union[float, None] = 0.025,
                             sulphur_content_lfo: Union[float, None] = 0.001,
                             sulphur_content_mgo: Union[float, None] = 0.001,
                             sulphur_content_lng: Union[float, None] = 0.00004
                             ) -> List[EmissionsEstimation]:
        """Retrieves a list of vessel emissions by its IMO.

        Args:
            imo: IMO of the vessel to retrieve emissions.
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics data in the response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics data in the response.
            include_eu_emissions: Include European Union related emissions data in the response.
            sulphur_content_hfo: Sulphur Content of HFO fuel type.
            sulphur_content_lfo: Sulphur Content of LFO fuel type.
            sulphur_content_mgo: Sulphur Content of MGO fuel type.
            sulphur_content_lng: Sulphur Content of LNG fuel type.

        Returns:
            A list of vessel emissions or None if no vessel with the specified IMO has
                been found.
        """
        query_url = self.construct_emissions_url_parameters(include_consumptions=include_consumptions,
                                                            include_efficiency_metrics=include_efficiency_metrics,
                                                            include_distances=include_distances,
                                                            include_durations=include_durations,
                                                            include_speed_statistics=include_speed_statistics,
                                                            include_eu_emissions=include_eu_emissions,
                                                            sulphur_content_hfo=sulphur_content_hfo,
                                                            sulphur_content_lfo=sulphur_content_lfo,
                                                            sulphur_content_mgo=sulphur_content_mgo,
                                                            sulphur_content_lng=sulphur_content_lng)
        query_url = urljoin(f"emissions/imo/{imo}", query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return [i for i in get_multiple(self.__connection, url, EmissionsEstimation)]

    def get_metrics_by_imo(self, imo: int, year: Union[int, None] = None) -> List[VesselMetrics]:
        """Get vessel metrics.

        Args:
            imo: Vessel IMO to retrieve
            year: The year for the annual metrics

        Returns:
            VesselMetrics for the requested IMO

        """
        url = urljoin(VesselEmissionsAPI.relative_url, f"emissions/metrics/imo/{imo}")
        if year is not None:
            url = urljoin(url, f"?year={year}")
        return [i for i in get_multiple(self.__connection, url, VesselMetrics)]

    def get_emissions_by_vessel_class_id(self,
                                         vessel_class_id: int,
                                         token: Union[str, None] = None,
                                         include_consumptions: bool = False,
                                         include_efficiency_metrics: bool = False,
                                         include_distances: bool = False,
                                         include_durations: bool = False,
                                         include_speed_statistics: bool = False,
                                         include_eu_emissions: bool = False) -> Optional[VesselClassEmissions]:
        """Get emissions estimations for a vessel class (supports incremental updates).

        Args:
            vessel_class_id: The vessel class to retrieve
            token: Next page token
            include_consumptions: Include consumption data in the response.
            include_efficiency_metrics: Include efficiency metrics data in the response.
            include_distances: Include distances data in the response.
            include_durations: Include duration data in the response.
            include_speed_statistics: Include speed statistics data in the response.
            include_eu_emissions: Include European Union related emissions data in the response.

        Returns:
            List of emissions estimation for all available voyages of a vessel class.

        """
        query_url = self.construct_emissions_url_parameters(token=token,
                                                            include_consumptions=include_consumptions,
                                                            include_efficiency_metrics=include_efficiency_metrics,
                                                            include_distances=include_distances,
                                                            include_durations=include_durations,
                                                            include_speed_statistics=include_speed_statistics,
                                                            include_eu_emissions=include_eu_emissions)
        query_url = urljoin(f"emissions/class/{vessel_class_id}", query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, VesselClassEmissions)

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
        query_url = urljoin(f"emissions/metrics/class/{vessel_class_id}", query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, VesselClassMetrics)
