# noqa: D100

from datetime import date
from typing import Optional, Tuple, cast

from .. import Connection
from .._internals import QueryString
from .vessel_classes import VESSEL_CLASSES
from .models import MarketRate, Route, VesselClass
from ._market_rates_json import parse_market_rates, parse_routes


class MarketRatesAPI:
    """Represents Signal's Market Rates API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Market Rates API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_market_rates(
        self, start_date: date, route_id: Optional[str] = None,
            vessel_class_id: Optional[int] = None,
            end_date: Optional[date] = None,
            is_clean: Optional[bool] = False
    ) -> Tuple[MarketRate, ...]:
        """Provides market rates for given day/period and route/vessel class.

        Args:
            start_date: Start date of market rates. If end date is not
            specified, it returns market rate for the given day only.
            route_id: Route ID.
            vessel_class_id: Vessel class ID.
            end_date: Combined with start_date will produce result market rates
            for all consecutive days from start to end date.

        Returns:
            The market rates or None if there are no market rates matching the
            given criteria.
        """
        query_dict = {
            "start_date": start_date.isoformat(),
            "is_clean": str(is_clean)
        }

        if route_id is not None:
            query_dict["route_id"] = '{}'.format(route_id)
        if vessel_class_id is not None:
            query_dict["vessel_class_id"] = '{}'.format(vessel_class_id)
        if end_date is not None:
            query_dict["end_date"] = end_date.isoformat()

        query_string: QueryString = query_dict
        response = self.__connection._make_get_request(
            "market-rates/api/market_rates", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_market_rates(response_json)

        return return_object

    def get_routes(
        self, vessel_class_id: Optional[int] = None
    ) -> Tuple[Route, ...]:
        """Fetches all routes or the ones matching the vessel class ID.

        Args:
            vessel_class_id: Vessel class ID.

        Returns:
            The result routes.
        """
        if vessel_class_id is not None:
            uri = f"market-rates/api/routes/{vessel_class_id}"
        else:
            uri = "market-rates/api/routes"

        response = self.__connection._make_get_request(uri)
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_routes(response_json)

        return return_object

    @staticmethod
    def get_vessel_classes() -> Tuple[VesselClass, ...]:
        """Retrieves all available vessel classes.

        Returns:
            A tuple of all available vessel classes.
        """
        vessel_types = tuple(VesselClass(
            cast(int, vessel_class["id"]),
            cast(int, vessel_class["vessel_type_id"]),
            cast(int, vessel_class["from_size"]),
            cast(int, vessel_class["to_size"]),
            cast(str, vessel_class["name"]),
            cast(str, vessel_class["vessel_type"]),
            cast(str, vessel_class["defining_size"]),
            cast(str, vessel_class["size"]))
                             for vessel_class in VESSEL_CLASSES)
        return vessel_types
