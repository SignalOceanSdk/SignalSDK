"""Base Scraped Data API class."""

from datetime import datetime
from typing import (
    Optional, List, Dict, Tuple, Type, Any, Generic, TypeVar)

from signal_ocean._internals import format_iso_datetime
from signal_ocean.connection import Connection
from signal_ocean.util.parsing_helpers import _to_camel_case
from signal_ocean.util.request_helpers import get_single

TRecord = TypeVar("TRecord")


class ScrapedDataResponse(Generic[TRecord]):
    """Base class for Scraped Data API response classes."""

    next_page_token: Optional[str]
    data: Optional[Tuple[TRecord, ...]]
    next_request_token: Optional[str] = None


class IncrementalDataResponse(Generic[TRecord]):
    """Base class for Incremental Data response classes."""

    data: Optional[Tuple[TRecord, ...]]
    next_request_token: Optional[str] = None


TResponse = TypeVar("TResponse", bound=ScrapedDataResponse[Any])


class ScrapedDataAPI(Generic[TResponse, TRecord]):
    """Base class for Scraped Data API classes."""

    page_size: int = 10000
    endpoints: Dict[str, str] = {
        "page_size": "?PageSize=" + str(page_size),
        "incremental": "/incremental?",
        "incremental_token": "/incremental/getincrementaltoken?",
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
                by page token.
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
            request_url: str = self._get_endpoint("page_size", params)

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

    def get_data_incremental(
            self,
            **params: Any,
    ) -> IncrementalDataResponse[TRecord]:
        """This function returns scraped data and next request token by given filters.

        Args:
            params: Return scraped data by provided parameters.
                Parameters are specified by outer functions.

        Returns:
            A dictionary containing a tuple of ScrapedData objects
            and NextRequestToken.
            ScrapedData object and NextRequestToken are defined
            by outer functions.
        """
        data: List[TRecord] = []
        results = IncrementalDataResponse[TRecord]()
        while True:
            request_url: str = self._get_endpoint("incremental", params)

            response: Optional[TResponse] = get_single(
                self.__connection, request_url, self.response_class
            )

            if response is not None and response.data is not None:
                data.extend(response.data)
            params["page_token"] = (
                response.next_page_token if response is not None else None
            )

            if params["page_token"] is None:
                results.data = tuple(data)
                results.next_request_token = (
                    response.next_request_token
                    if response is not None else None
                )
                break

        return results

    def get_data_incremental_token(
            self,
            updated_date_from: datetime
    ) -> Optional[str]:
        """This function returns a token to use in the incremental data endpoints.

        Args:
            updated_date_from: Format - date-time (as date-time in RFC3339).
                Earliest date the cargo updated.
                Cannot be combined with 'Received' dates

        Returns:
            A string containing the corresponding page token to
            the provided datetime input.
        """
        request_url: str = self._get_endpoint(
            "incremental_token", {"updated_date_from": updated_date_from}
        )

        return get_single(self.__connection, request_url, str)
