# noqa: D100

from datetime import date
from typing import Optional, Tuple, List

from .. import Connection
from .._internals import QueryString
from .enums import VesselClass
from .models import FreightPricing, Port
from .port_filter import PortFilter
from ._freight_rates_json import parse_freight_pricing, parse_ports


class FreightRatesAPI:
    """Represents Signal's Freight Rates API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Freight Rates API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_freight_pricing(
            self, load_ports: List[int], discharge_ports: List[int],
            vessel_classes: List[str], is_clean: bool,
            date: date = date.today()
    ) -> Tuple[FreightPricing, ...]:
        """Provides freight pricing for given load/discharge ports.

        Args:
            load_ports: Load ports.
            discharge_ports: Discharge ports.
            vessel_classes: Vessel classes for which to return the freight e.g.
            VLCC, Aframax etc.
            is_clean: True if it is clean cargo.
            date: Date of pricing.


        Returns:
            The freight pricing or None if there are is no freight matching the
            given criteria.
        """
        query_dict = {
            "LoadPorts": '&LoadPorts='.join([str(lp) for lp in load_ports]),
            "DischargePorts": '&DischargePorts='.join([str(dp) for dp in
                                                       discharge_ports]),
            "IsClean": '{}'.format(is_clean),
            "Date": date.isoformat()
        }

        vessel_classes_param = '&VesselClasses='.join(vessel_classes)
        query_dict['VesselClasses'] = vessel_classes_param

        query_string: QueryString = query_dict
        response = self.__connection._make_get_request(
            "freight/api/Freight/v3/pricing", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_freight_pricing(response_json)

        return return_object

    @staticmethod
    def get_vessel_classes() -> Tuple[str, ...]:
        """Retrieves all available vessel classes.

        Returns:
            A tuple of all available vessel classes.
        """
        vessel_classes = tuple(vessel_class.name
                               for vessel_class in VesselClass)
        return vessel_classes

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
        query_dict = {
            "date": date.today().isoformat()
        }

        query_string: QueryString = query_dict

        available_ports: List[Port] = []
        for vessel_class in VesselClass:
            response = self.__connection._make_get_request(
                f"freight/api/Freight/v2/pricing/"
                f"availablePorts/{vessel_class.name}",
                query_string
            )
            response.raise_for_status()
            response_json = response.json()
            available_ports += parse_ports(response_json)

        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(available_ports))
