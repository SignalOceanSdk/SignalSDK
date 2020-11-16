"""Helper functions to retrieve data from APIs."""
from typing import TypeVar, Tuple, Type, Optional, Dict

import requests

from signal_ocean import Connection
from signal_ocean._internals import QueryString
from signal_ocean.util.parsing_helpers import parse_model


TModel = TypeVar("TModel")


def get_single(connection: Connection, relative_url: str, cls: Type[TModel],
               query_string: Optional[QueryString] = None,
               rename_keys: Optional[Dict[str, str]] = None) \
        -> Optional[TModel]:
    """Get a single object from the API.

    Make a get request to the specified URL and return an object of the
    provided class instantiated with the retrieved data. If the API responds
    with a "Not Found" status code, return None.

    Args:
        connection: The connection object to use to make the appropriate get
            request to the API.
        relative_url: The relative URL to make the request to.
        cls: The class to instantiate the object for the retrieved data.
        query_string: Query parameters for the request.
        rename_keys: Key names to rename to match model attribute names,
            used when an automated translation of the name from CapsWords
            to snake_case is to sufficient. Renaming must provide the name
            in CapsWords.

    Returns:
        An object of the provided class instantiated with the data retrieved
        from the specified URL, or None if the API responds with a "Not Found"
        status code.
    """
    response = connection._make_get_request(relative_url,
                                            query_string=query_string)

    if response.status_code == requests.codes.not_found:
        return None

    response.raise_for_status()
    data = response.json()
    return parse_model(data, cls, rename_keys=rename_keys)


def get_multiple(connection: Connection, relative_url: str, cls: Type[TModel],
                 query_string: Optional[QueryString] = None,
                 rename_keys: Optional[Dict[str, str]] = None) \
        -> Tuple[TModel, ...]:
    """Get a multiple objects from the API.

    Make a get request to the specified URL to retrieve a sequence of results
    and return a list of objects of the provided class instantiated with the
    retrieved data. If the API responds with an empty sequence an empty list
    is returned.

    Args:
        connection: The connection object to use to make the appropriate get
            request to the API.
        relative_url: The relative URL to make the request to.
        cls: The class to instantiate the object for the retrieved data.
        query_string: Query parameters for the request.
        rename_keys: Key names to rename to match model attribute names,
            used when an automated translation of the name from CapsWords
            to snake_case is to sufficient. Renaming must provide the name
            in CapsWords.
    """
    response = connection._make_get_request(relative_url,
                                            query_string=query_string)
    response.raise_for_status()
    data = response.json()
    return tuple(parse_model(d, cls, rename_keys=rename_keys) for d in data)
