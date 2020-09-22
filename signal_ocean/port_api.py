# noqa: D100

from typing import Tuple, Optional

from .connection import Connection
from .port import Port
from .port_filter import PortFilter


class PortAPI:
    """Represents Signal's Port API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Port API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

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
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))
