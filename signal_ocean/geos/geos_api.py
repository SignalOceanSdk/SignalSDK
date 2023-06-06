"""The geos api."""
from typing import Optional, Tuple
from urllib.parse import urljoin
from datetime import date
from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single
from signal_ocean.geos.models import GeoAsset, Port, Country, Area
from signal_ocean.geos.models import AreasPagedResponse
from signal_ocean.geos.models import GeoAssetsPagedResponse
from signal_ocean.geos.models import CountriesPagedResponse, PortsPagedResponse


class GeosAPI:
    """Represents Signal's Geos API."""

    relative_url = "geos-api/v2/"
    default_pit = str(date.today())

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes GeosAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_areas(self, areaId: Optional[int] = None) -> Tuple[Area, ...]:
        """Retrieves all available areas.

        Args:
            areaId: area identifier to filter and return only a
                specific area.

        Returns:
            A tuple of all available areas.
        """
        endpoint = (
            "areas/all" if areaId is None else f"areas/{areaId}"
        )

        url = urljoin(GeosAPI.relative_url, endpoint)
        response = get_single(self.__connection, url, AreasPagedResponse)

        if response is not None and response.data is not None:
            return response.data
        else:
            return tuple([])

    def get_geoAssets(
        self,
        geoAssetId: Optional[int] = None
    ) -> Tuple[GeoAsset, ...]:
        """Retrieves all available geo assets.

        Args:
            geoAssetId: geo asset identifier to filter and return only a
                specific geo asset.

        Returns:
            A tuple of all available geo asset.
        """
        endpoint = (
            "geoAssets/all" if geoAssetId is None
            else f"geoAssets/{geoAssetId}"
        )
        rename_keys = {
            "AreaIDLevel0": "area_id_level0",
            "AreaIDLevel1": "area_id_level1",
            "AreaIDLevel2": "area_id_level2",
            "AreaIDLevel3": "area_id_level3",
            "CountryCodeISO3": "country_code_iso3"}
        url = urljoin(GeosAPI.relative_url, endpoint)
        response = get_single(
            self.__connection,
            url,
            GeoAssetsPagedResponse,
            rename_keys=rename_keys)
        if response is not None and response.data is not None:
            return response.data
        else:
            return tuple([])

    def get_countries(
        self,
        countryId: Optional[int] = None
    ) -> Tuple[Country, ...]:
        """Retrieves all available countries.

        Args:
            countryId: country identifier to filter and return only a
                specific country.

        Returns:
            A tuple of all available countries.
        """
        endpoint = (
            "countries/all" if countryId is None else f"countries/{countryId}"
        )
        url = urljoin(GeosAPI.relative_url, endpoint)
        response = get_single(self.__connection, url, CountriesPagedResponse)
        if response is not None and response.data is not None:
            return response.data
        else:
            return tuple([])

    def get_ports(self, portId: Optional[int] = None) -> Tuple[Port, ...]:
        """Retrieves all available ports.

        Args:
            portId: port identifier to filter and return only a
                specific port.

        Returns:
            A tuple of all available ports.
        """
        endpoint = (
            "ports/all" if portId is None else f"ports/{portId}"
        )
        rename_keys = {
            "AreaIDLevel0": "area_id_level0",
            "AreaIDLevel1": "area_id_level1",
            "AreaIDLevel2": "area_id_level2",
            "AreaIDLevel3": "area_id_level3"}
        url = urljoin(GeosAPI.relative_url, endpoint)
        response = get_single(
            self.__connection,
            url,
            PortsPagedResponse,
            rename_keys=rename_keys)
        if response is not None and response.data is not None:
            return response.data
        else:
            return tuple([])
