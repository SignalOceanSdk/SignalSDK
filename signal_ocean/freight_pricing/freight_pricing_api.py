# noqa: D100

from datetime import date
from typing import Tuple, Optional

from .. import Connection, Port
from .._internals import format_iso_date
from .vessel_type import VesselType
from .vessel_subclass import VesselSubclass
from .models import FreightPricing
from . import _freight_pricing_json


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
            vessel_subclass: VesselSubclass) -> Tuple[FreightPricing, ...]:
        """Retrieves freight prices for moving commodities between two ports.

        Args:
            vessel_type: The type of vessel to calculate the prices for.
            load_port: Port where the commodity is loaded.
            discharge_port: Port where the commodity is discharged.
            date: Date at which the freight price is requested.
            vessel_subclass: The vessel's subclass.

        Returns:
            A tuple of freight pricings, one per vessel class.
        """
        query_string = {
            'vesselType': vessel_type.value,
            'loadPortId': load_port.id,
            'dischargePortId': discharge_port.id,
            'date': format_iso_date(date),
            'vesselSubclass': vessel_subclass.value
        }
        response = self.__connection._make_get_request(
            'freight-pricing/FreightPricing',
            query_string
        )
        response.raise_for_status()

        return _freight_pricing_json.parse(response.json())
