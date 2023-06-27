"""The vessel emissions api."""
from typing import Optional, List, Union
from urllib.parse import urljoin
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_multiple, get_single
from signal_ocean.vessel_emissions.models import EmissionsEstimationModel, VesselMetrics, VesselClassEmissions, \
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

    def construct_emissions_url(self,
                                year: int = None,
                                quantity: int = None,
                                token: str = None,
                                include_consumptions: bool = False,
                                include_efficiency_metrics: bool = False,
                                include_distances: bool = False,
                                include_durations: bool = False,
                                include_speed_statistics: bool = False,
                                include_eu_emissions: bool = False,
                                sulphur_content_hfo: float = None,
                                sulphur_content_lfo: float = None,
                                sulphur_content_mgo: float = None,
                                sulphur_content_lng: float = None):
        """

        Args:
            year:
            quantity:
            token:
            include_consumptions:
            include_efficiency_metrics:
            include_distances:
            include_durations:
            include_speed_statistics:
            include_eu_emissions:
            sulphur_content_hfo:
            sulphur_content_lfo:
            sulphur_content_mgo:
            sulphur_content_lng:

        Returns:

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
                                               quantity: int = None,
                                               include_consumptions: bool = False,
                                               include_efficiency_metrics: bool = False,
                                               include_distances: bool = False,
                                               include_durations: bool = False,
                                               include_speed_statistics: bool = False,
                                               include_eu_emissions: bool = False,
                                               sulphur_content_hfo: float = None,
                                               sulphur_content_lfo: float = None,
                                               sulphur_content_mgo: float = None,
                                               sulphur_content_lng: float = None
                                               ) -> Optional[EmissionsEstimationModel]:
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
            EmissionsEstimationModel if no vessel with the specified IMO or Voyage Number has
                been found.
        """
        query_url = self.construct_emissions_url(quantity=quantity,
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
        return get_single(self.__connection, url, EmissionsEstimationModel)

    def get_emissions_by_imo(self, imo: int,
                             include_consumptions: bool = False,
                             include_efficiency_metrics: bool = False,
                             include_distances: bool = False,
                             include_durations: bool = False,
                             include_speed_statistics: bool = False,
                             include_eu_emissions: bool = False,
                             sulphur_content_hfo: float = 0.1,
                             sulphur_content_lfo: float = 0.1,
                             sulphur_content_mgo: float = 0.1,
                             sulphur_content_lng: float = 0.1
                             ) -> List[EmissionsEstimationModel]:
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
        query_url = self.construct_emissions_url(include_consumptions=include_consumptions,
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
        return [i for i in get_multiple(self.__connection, url, EmissionsEstimationModel)]

    def get_metrics_by_imo(self, imo: int, year: int) -> List[VesselMetrics]:
        url = urljoin(VesselEmissionsAPI.relative_url, f"emissions/metrics/imo/{imo}")
        return [i for i in get_multiple(self.__connection, url, VesselMetrics)]

    def get_emissions_by_vessel_class_id(self,
                                         vessel_class_id: int,
                                         token: str = None,
                                         include_consumptions: bool = False,
                                         include_efficiency_metrics: bool = False,
                                         include_distances: bool = False,
                                         include_durations: bool = False,
                                         include_speed_statistics: bool = False,
                                         include_eu_emissions: bool = False) -> Optional[VesselClassEmissions]:
        query_url = self.construct_emissions_url(token=token,
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
                                       year: int = None,
                                       token: str = None
                                       ) -> Optional[VesselClassMetrics]:
        query_url = "?"
        if year:
            query_url += f"year={year}"
        if token:
            query_url += f"&token={token}"
        query_url = urljoin(f"emissions/metrics/class/{vessel_class_id}", query_url)
        url = urljoin(VesselEmissionsAPI.relative_url, query_url)
        return get_single(self.__connection, url, VesselClassMetrics)
