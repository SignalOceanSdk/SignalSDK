from typing import List
from urllib.parse import urljoin

import requests

from .connection import Connection
from .port import Port
from .port_filter import PortFilter


class PortAPI:
    def __init__(self, connection: Connection = None):
        self.__connection = connection or Connection()

    def get_ports(self, port_filter: PortFilter = None) -> List[Port]:
        url = urljoin(
            self.__connection.api_host,
            'htl-api/historical-tonnage-list/ports'
        )

        response = requests.get(url, headers=self.__connection.headers)
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return list(port_filter._apply(ports))

