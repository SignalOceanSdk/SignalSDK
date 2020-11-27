# noqa: D100

from datetime import datetime
from typing import Optional

from .. import Connection
from .._internals import QueryString
from .models import PortExpenses, CanalExpenses
from ._port_expenses_json import parse_port_expenses, parse_canal_expenses


class PortExpensesAPI:
    """Represents Signal's Port Expenses API."""

    def __init__(self, connection: Optional[Connection] = None):
        """Initializes the Port Expenses API.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()

    def get_port_expenses(
        self, imo: int, port_id: int, group_id: int = 1) -> PortExpenses:
        """Retrieves port expenses.

        Args:
            imo: The vessel's IMO number.
            port_id: ID of the port to retrieve the expenses for.
            group_id: Group ID.

        Returns:
            The port expenses or None if a port with given ID does not exist or
            a vessel with the given IMO number does not exist.
        """
        query_string: QueryString = {
            "imo": '{}'.format(imo),
            "portId": '{}'.format(port_id),
            "groupId": '{}'.format(group_id)
        }

        response = self.__connection._make_post_request(
            "port-expenses/api/v1/Port", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_port_expenses(response_json) if response_json else None

        return return_object

    def get_canal_expenses(
        self, canal: int, imo: int, open_port_id: int, load_port_id: int,
            discharge_port_id: int, ballast_speed: float, laden_speed: float,
            operation_status: int, formula_calculation_date: datetime,
            open_date: datetime, load_sail_date: datetime,
            cargo_type: Optional[str] = None) -> CanalExpenses:
        """Retrieves canal expenses.

        Args:
            canal
            imo
            open_port_id
            load_port_id
            discharge_port_id
            ballast_speed
            laden_speed
            operation_status
            formula_calculation_date
            open_date
            load_sail_date
            cargo_type

        Returns:
            The canal expenses or None if expenses can be provided for the
            given parameters.
        """
        query_string: QueryString = {
            "canal": '{}'.format(canal),
            "imo": '{}'.format(imo),
            "openPortId": '{}'.format(open_port_id),
            "loadPortId": '{}'.format(load_port_id),
            "dischargePortId": '{}'.format(discharge_port_id),
            "ballastSpeed": '{}'.format(ballast_speed),
            "ladenSpeed": '{}'.format(laden_speed),
            "operationStatus": '{}'.format(operation_status),
            "formulaCalculationDate": formula_calculation_date.isoformat(),
            "openDate": open_date.isoformat(),
            "loadSailDate": load_sail_date.isoformat(),
            "cargoType": cargo_type
        }

        response = self.__connection._make_post_request(
            "port-expenses/api/v1/Canal", query_string
        )
        response.raise_for_status()
        response_json = {"TotalCost": response.json()}
        return_object = parse_canal_expenses(response_json) if response_json else None

        return return_object