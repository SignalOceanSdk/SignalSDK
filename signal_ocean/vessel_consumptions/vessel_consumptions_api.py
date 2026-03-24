"""The vessel consumptions api."""
import os
import copy
from typing import Optional, Type, TypeVar, Union
from urllib.parse import urljoin, urlencode

import requests

from signal_ocean import Connection
from signal_ocean.vessel_consumptions.models import (
    VesselConsumptions,
    AdvertisedConsumptions,
    AdvertisedConsumptionsPage,
)

TModel = TypeVar("TModel")


def make_url(
        base_url: str,
        *res: Union[str, int],
        **params: str
) -> str:
    """Constructs url for the request.

    Args:
        base_url: the base to build the url.

    """
    url = base_url
    for r in res:
        url = '{}/{}'.format(url, r)
    if params:
        url = '{}?{}'.format(url, urlencode(params))
    return url


def custom_headers(connection: Connection) -> dict:
    """Custom function to change the request header.

    Args:
        connection: Connection object

    Returns:
        headers dict

    """
    return {
        "Api-Key":
            connection._Connection__api_key  # type: ignore
            or os.environ.get("SIGNAL_OCEAN_API_KEY"),
        "Content-Type": "application/json",
        "Source": "SignalSDK",
    }


class VesselConsumptionsAPI:
    """Represents Signal's Vessel Consumptions API."""

    relative_url = "vessel-consumptions-api/v1/"

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes VesselConsumptionsAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        if connection is not None:
            vc_connection = copy.deepcopy(connection)
            func_type = type(
                vc_connection._Connection__get_headers  # type: ignore
            )
            vc_connection._Connection__get_headers = func_type(  # type: ignore
                custom_headers, vc_connection
            )
            self.__connection = vc_connection
        else:
            connection = Connection()
            func_type = type(
                connection._Connection__get_headers  # type: ignore
            )
            connection._Connection__get_headers = func_type(  # type: ignore
                custom_headers, connection
            )
            self.__connection = connection

    def __get_single(
            self,
            relative_url: str,
            cls: Type[TModel]
    ) -> Optional[TModel]:
        response = self.__connection._make_get_request(relative_url)

        if response.status_code in (
            requests.codes.not_found,
            requests.codes.no_content,
        ):
            return None

        response.raise_for_status()
        data = response.json()
        return cls.model_validate(data)  # type: ignore[attr-defined]

    def get_consumptions(
            self,
            imo: int
    ) -> Optional[VesselConsumptions]:
        """Retrieves vessel consumptions by IMO.

        Args:
            imo: Vessel IMO to retrieve consumptions for.

        Returns:
            VesselConsumptions or None if no vessel with
            the specified IMO has been found.
        """
        query_url = make_url('vessels', imo, 'consumptions')
        url = urljoin(VesselConsumptionsAPI.relative_url, query_url)
        return self.__get_single(url, VesselConsumptions)

    def get_advertised_consumptions(
            self,
            imo: int
    ) -> Optional[AdvertisedConsumptions]:
        """Retrieves advertised consumptions by IMO.

        Args:
            imo: Vessel IMO to retrieve advertised consumptions for.

        Returns:
            AdvertisedConsumptions or None if no vessel with
            the specified IMO has been found.
        """
        query_url = make_url('vessels', imo, 'advertisedConsumptions')
        url = urljoin(VesselConsumptionsAPI.relative_url, query_url)
        return self.__get_single(url, AdvertisedConsumptions)

    def get_advertised_consumptions_paginated(
            self,
            token: Optional[str] = None,
            page_size: Optional[int] = None
    ) -> Optional[AdvertisedConsumptionsPage]:
        """Retrieves a paginated list of all advertised consumptions.

        Args:
            token: Next page token for pagination.
            page_size: Number of results per page.

        Returns:
            AdvertisedConsumptionsPage containing advertised consumptions
            and a token for the next page.
        """
        params = {}
        if token is not None:
            params['token'] = token
        if page_size is not None:
            params['pageSize'] = str(page_size)
        query_url = make_url('vessels', 'advertisedConsumptions', **params)
        url = urljoin(VesselConsumptionsAPI.relative_url, query_url)
        return self.__get_single(url, AdvertisedConsumptionsPage)
