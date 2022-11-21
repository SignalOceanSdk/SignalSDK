"""Base Scraped Data API class."""

from datetime import datetime
from typing import Optional, List, Dict, Tuple, Type, Any, Generic, TypeVar

from signal_ocean._internals import format_iso_datetime
from signal_ocean.connection import Connection
from signal_ocean.util.parsing_helpers import _to_camel_case
from signal_ocean.util.request_helpers import get_single

TRecord = TypeVar("TRecord")


class ScrapedDataResponse(Generic[TRecord]):
    """Base class for Scraped Data API response classes."""
    next_page_token: Optional[str]
    data: Optional[Tuple[TRecord, ...]]


TResponse = TypeVar("TResponse", bound=ScrapedDataResponse[Any])


class ScrapedDataAPI(Generic[TResponse, TRecord]):
    """Base class for Scraped Data API classes."""

    page_size = 10000
    endpoints = {
        "page_size": "?PageSize=" + str(page_size),
        "by_id": "/getbyids?",
    }
    relative_url: str
    response_class: Type[TResponse]

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Scraped Data API.

        Args:
            connection: API connection configuration.
                If not provided, the default connection method is used.
        """
        self.__connection = connection or Connection()

    def _get_endpoint(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generates the endpoint to call to retrieve requested scraped data.

        Args:
            endpoint: Define endpoint to use. It could be either by filters or
                by entity ids.
            params: Return scraped data by provided parameters.

        Returns:
            The endpoint to call in order to retrieve the scraped data
            for provided parameters.
        """
        url = self.relative_url + self.endpoints[endpoint]

        for param, value in params.items():
            if value:
                if isinstance(value, str):
                    pass
                elif isinstance(value, List):
                    value = ",".join(map(str, value))
                elif isinstance(value, datetime):
                    value = format_iso_datetime(value)
                else:
                    value = str(value)

                url += (
                    ("" if url[-1] == "?" else "&")
                    + _to_camel_case(param)
                    + "="
                    + value
                )
        return url

    def get_data(self, **params: Any) -> Tuple[TRecord, ...]:
        """This function collects and returns scraped data by given filters.

        Args:
            params: Return scraped data by provided parameters.
                Parameters are specified by outer functions.

        Returns:
            A tuple containing ScrapedData objects.
            ScrapedData object are defined by outer class.
        """
        results: List[TRecord] = []
        while True:
            request_url = self._get_endpoint("page_size", params)

            response: Optional[TResponse] = get_single(
                self.__connection, request_url, self.response_class
            )

            if response is not None and response.data is not None:
                results.extend(response.data)
            params["page_token"] = (
                response.next_page_token if response is not None else None
            )

            if params["page_token"] is None:
                break

        return tuple(results)

    def get_data_by_entity_ids(self, **params: Any) -> Tuple[TRecord, ...]:
        """This function collects and returns scraped data by given entity ids.

        Args:
            params: Return scraped data by provided parameters.
                Parameters are specified by outer functions.

        Returns:
            A tuple containing ScrapedData objects.
            ScrapedData object are defined by outer class.
        """
        results: List[TRecord] = []
        request_url = self._get_endpoint("by_id", params)

        response: Optional[TResponse] = get_single(
            self.__connection, request_url, self.response_class
        )

        if response is not None and response.data is not None:
            results.extend(response.data)

        return tuple(results)
