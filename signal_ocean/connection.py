# noqa: D100

import os
from typing import Optional


class Connection:
    """Facilitates authenticated communication with Signal APIs."""

    __DEFAULT_API_HOST = 'https://signalprodapims.azure-api.net/'

    def __init__(self, api_key: Optional[str] = None, api_host: Optional[str] = None):
        """Initializes the connection.

        Args:
            api_key: The API subscription key retrieved from Signal's API
                developer portal. If not provided, will be retrieved from the
                SIGNAL_OCEAN_API_KEY environment variable.
            api_host: Used to override the base URL used to contact the APIs. If
                not provided, can be overridden by the SIGNAL_OCEAN_API_HOST
                environment variable. If the environment variable is not
                defined, the base URL will fall back to where Signal's APIs are
                hosted.
        """
        self.__api_key = api_key
        self.__api_host = api_host

    @property
    def _headers(self):
        return {
            'Api-Key': self.__api_key or os.environ.get('SIGNAL_OCEAN_API_KEY'),
            'Content-Type': 'application/json'
        }

    @property
    def _api_host(self):
        return (
            self.__api_host
            or os.environ.get('SIGNAL_OCEAN_API_HOST')
            or Connection.__DEFAULT_API_HOST
        )
