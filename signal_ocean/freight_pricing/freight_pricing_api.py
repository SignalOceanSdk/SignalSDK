# noqa: D100

from datetime import date
from urllib.parse import urljoin

import requests

from .. import Connection, Port
from .._internals import format_iso_date
from .vessel_type import VesselType
from .vessel_subclass import VesselSubclass
from .freight_pricing import FreightPricing
from . import _freight_pricing_json


class FreightPricingAPI:
    """Represents Signal's Freight Pricing API."""

    def __init__(self, connection: Connection = None):
        """Freight Pricing API.

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
            vessel_subclass: VesselSubclass) -> FreightPricing:
        """Retrieves freight prices for moving commodities between two ports.

        Args:
            vessel_type: The type of vessel to calculate the prices for.
            load_port: Port where the commodity is loaded.
            discharge_port: Port where the commodity is discharged.
            date: Date at which the freight price is requested.
            vessel_subclass: The vessel's subclass.

        Returns:
            A collection of freight pricing items, one per vessel class.
        """
        url = urljoin(
            self.__connection._api_host,
            'freight-pricing/FreightPricing'
        )
        query_string = {
            'vesselType': vessel_type.value,
            'loadPortId': load_port.id,
            'dischargePortId': discharge_port.id,
            'date': format_iso_date(date),
            'vesselSubclass': vessel_subclass.value
        }
        response = requests.get(
            url,
            params=query_string,
            headers=self.__connection._headers
        )
        response.raise_for_status()

        return _freight_pricing_json.parse(response.json())
