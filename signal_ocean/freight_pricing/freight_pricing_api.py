# noqa: D100

from datetime import date
from typing import Tuple, Optional, Dict, Any

from .. import Connection
from .._internals import format_iso_date
from .vessel_subclass import VesselSubclass
from .models import FreightPricing
from . import _freight_pricing_json
from .port import Port
from .port_filter import PortFilter
from .vessel_class import VesselClass
from .vessel_class_filter import VesselClassFilter
from .vessel_type import VesselType
from .vessel_type_filter import VesselTypeFilter


class FreightPricingAPI:
    """Represents Signal's Freight Pricing API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes FreightPricingAPI.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_freight_pricing(
            self,
            vessel_type: VesselType,
            load_port: Port,
            discharge_port: Port,
            date: date,
            vessel_subclass: Optional[VesselSubclass] = None,
            vessel_classes: Optional[Tuple[VesselClass, ...]] = None
            ) -> Tuple[FreightPricing, ...]:
        """Retrieves freight prices for moving commodities between two ports.

        Args:
            vessel_type: The type of vessel to calculate the prices for.
            load_port: Port where the commodity is loaded.
            discharge_port: Port where the commodity is discha
            rged.
            date: Date at which the freight price is requested.
            vessel_subclass: The vessel's subclass. This is an optional
             parameter.
            vessel_class: The vessel's class. You can set multiple vessel
             classes.

        Returns:
            A tuple of freight pricings, one per vessel class.
        """
        query_string: Dict[str, Any] = {
            'vesselType': vessel_type.id,
            'loadPortId': load_port.id,
            'dischargePortId': discharge_port.id,
            'date': format_iso_date(date)
        }

        if vessel_classes is not None:
            query_string['vesselClassId'] = [
                vc.id for vc in vessel_classes]

        if vessel_subclass is not None:
            query_string['vesselSubclass'] = vessel_subclass.value

        response = self.__connection._make_get_request(
            'freight-pricing-api/freight-pricing',
            query_string
        )
        response.raise_for_status()
        return _freight_pricing_json.parse(response.json())

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
            "freight-pricing-api/ports"
        )
        response.raise_for_status()

        ports = (Port(**p) for p in response.json())
        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(ports))

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
            "freight-pricing-api/vessel-classes"
        )
        response.raise_for_status()

        classes = (VesselClass(**c) for c in response.json())
        class_filter = class_filter or VesselClassFilter()

        return tuple(class_filter._apply(classes))

    def get_vessel_types(
        self, type_filter: Optional[VesselTypeFilter] = None
    ) -> Tuple[VesselType, ...]:
        """Retrieves available vessel types.

        Args:
            type_filter: A filter used to find specific vessel types. If not
                specified, returns all available vessel types.

        Returns:
            A tuple of available vessel types that match the filter.
        """
        response = self.__connection._make_get_request(
            "freight-pricing-api/vessel-types"
        )
        response.raise_for_status()

        types = (VesselType(**c) for c in response.json())
        type_filter = type_filter or VesselTypeFilter()

        return tuple(type_filter._apply(types))
