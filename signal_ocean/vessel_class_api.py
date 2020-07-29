# noqa: D100

from typing import List, Optional
from urllib.parse import urljoin

import requests

from .connection import Connection
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter


class VesselClassAPI:
    """Represents Signal's Vessel Class API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Vessel Class API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_vessel_classes(
            self,
            class_filter: Optional[VesselClassFilter] = None) -> List[VesselClass]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If not
                specified, returns all available vessel classes.

        Returns:
            A list of available vessel classes that match the filter.
        """
        url = urljoin(
            self.__connection._api_host,
            'htl-api/historical-tonnage-list/vessel-classes'
        )

        response = requests.get(url, headers=self.__connection._headers)
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return list(class_filter._apply(classes))
