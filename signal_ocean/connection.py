# noqa: D100

import json
import os
from typing import Optional, Dict
from urllib.parse import urljoin

import requests

from ._internals import QueryString


class Connection:
    """Facilitates authenticated communication with Signal APIs."""

    __DEFAULT_API_HOST = "https://api-gateway.signalocean.com/"

    def __init__(
        self, api_key: Optional[str] = None, api_host: Optional[str] = None
    ):
        """Initializes the connection.

        Args:
            api_key: The API subscription key retrieved from Signal's API
                developer portal. If not provided, will be retrieved from the
                SIGNAL_OCEAN_API_KEY environment variable.
            api_host: Used to override the base URL used to contact the APIs.
                If not provided, can be overridden by the SIGNAL_OCEAN_API_HOST
                environment variable. If the environment variable is not
                defined, the base URL will fall back to where Signal's APIs are
                hosted.
        """
        self.__api_key = api_key
        self.__api_host = api_host

    def __get_headers(self) -> Dict[str, Optional[str]]:
        api_key = self.__api_key or os.environ.get("SIGNAL_OCEAN_API_KEY")

        return {
            "Api-Key": api_key,
            "Content-Type": "application/json",
            "Source": "SignalSDK",
        }

    def __get_api_host(self) -> str:
        host = (
            self.__api_host
            or os.environ.get("SIGNAL_OCEAN_API_HOST")
            or Connection.__DEFAULT_API_HOST
        )

        return host if host.endswith("/") else host + "/"

    def _make_get_request(
        self, relative_url: str, query_string: Optional[QueryString] = None
    ) -> requests.Response:
        url = urljoin(self.__get_api_host(), relative_url)

        # Ignoring "params" type because None is acceptable according to
        # https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
        # but the stub file does not include it
        return requests.get(
            url,
            params=query_string,  # type: ignore
            headers=self.__get_headers(),
        )

    def _make_post_request(
        self, relative_url: str, query_string: Optional[QueryString] = None
    ) -> requests.Response:
        url = urljoin(self.__get_api_host(), relative_url)

        return requests.post(
            url,
            data=json.dumps(query_string),
            headers=self.__get_headers(),
        )
