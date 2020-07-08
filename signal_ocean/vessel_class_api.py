from typing import List
from urllib.parse import urljoin

import requests

from .connection import Connection
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter


class VesselClassAPI:
    def __init__(self, connection: Connection = None):
        self.__connection = connection or Connection()

    def get_vessel_classes(self, class_filter: VesselClassFilter = None) -> List[VesselClass]:
        url = urljoin(
            self.__connection.api_host,
            'htl-api/historical-tonnage-list/vessel-classes'
        )

        response = requests.get(url, headers=self.__connection.headers)
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return list(class_filter._apply(classes))
