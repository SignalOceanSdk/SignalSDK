# noqa: D100

from typing import Optional, Tuple, TypeVar, Callable

import requests

from .. import Connection
from .models import Country, Port, Area
from .port_filter import PortFilter
from . import _geo_json

TModel = TypeVar("TModel")
JsonParser = Callable[[dict], TModel]


class GeoAPI:
    """Represents Signal's Geo API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes GeoAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def __get_multiple(
        self, url: str, parse_json: JsonParser[TModel]
    ) -> Tuple[TModel, ...]:
        response = self.__connection._make_get_request(url)
        response.raise_for_status()

        return tuple(parse_json(j) for j in response.json())

    def __get_single(
        self, url: str, parse_json: JsonParser[TModel]
    ) -> Optional[TModel]:
        response = self.__connection._make_get_request(url)
        if response.status_code == requests.codes.not_found:
            return None

        response.raise_for_status()
        return parse_json(response.json())

    def get_countries(self) -> Tuple[Country, ...]:
        """Retrieves all available countries.

        Returns:
            A tuple of all available countries.
        """
        return self.__get_multiple("geo/countries", _geo_json.parse_country)

    def get_country(self, country_id: int) -> Optional[Country]:
        """Retrieves a country by its ID.

        Args:
            country_id: ID of the country to retrieve.

        Returns:
            A country or None if no country with the specified ID has been
            found.
        """
        return self.__get_single(
            f"geo/countries/{country_id}", _geo_json.parse_country
        )

    def get_ports(
        self, port_filter: Optional[PortFilter] = None
    ) -> Tuple[Port, ...]:
        """Retrieves available ports.

        Args:
            port_filter: A filter used to find specific ports. If not
                specified, returns all available ports.

        Returns:
            A tuple of available ports that match the filter.
        """
        ports = self.__get_multiple("geo/ports", _geo_json.parse_port)
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

    def get_port(self, port_id: int) -> Optional[Port]:
        """Retrieves a port by its ID.

        Args:
            port_id: ID of the port to retrieve.

        Returns:
            A port or None if no port with the specified ID has been found.
        """
        return self.__get_single(f"geo/ports/{port_id}", _geo_json.parse_port)

    def get_areas(self) -> Tuple[Area, ...]:
        """Retrieves all available areas.

        Returns:
            A tuple of all available areas.
        """
        return self.__get_multiple("geo/areas", _geo_json.parse_area)

    def get_area(self, area_id: int) -> Optional[Area]:
        """Retrieves a area by its ID.

        Args:
            area_id: ID of the area to retrieve.

        Returns:
            A area or None if no area with the specified ID has been found.
        """
        return self.__get_single(f"geo/areas/{area_id}", _geo_json.parse_area)
