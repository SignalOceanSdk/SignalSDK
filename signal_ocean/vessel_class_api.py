# noqa: D100

from typing import Tuple, Optional
import warnings

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
        warnings.warn(
            "signal_ocean.VesselClassAPI is deprecated and will be removed in "
            "a future version of the SDK. Please use "
            "tonnage_list.TonnageListAPI to get vessel classes instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        self.__connection = connection or Connection()

    def get_vessel_classes(
        self, class_filter: Optional[VesselClassFilter] = None
    ) -> Tuple[VesselClass, ...]:
        """Retrieves available vessel classes.

        Args:
            class_filter: A filter used to find specific vessel classes. If not
                specified, returns all available vessel classes.

        Returns:
            A tuple of available vessel classes that match the filter.
        """
        response = self.__connection._make_get_request(
            "htl-api/historical-tonnage-list/vessel-classes"
        )
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))
