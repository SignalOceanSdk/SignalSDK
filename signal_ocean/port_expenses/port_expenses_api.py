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
        self, imo: int, port_id: int, group_id: int = 1
    ) -> Optional[PortExpenses]:
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
        return_object = parse_port_expenses(response_json) \
            if response_json else None

        return return_object

    def get_canal_expenses(
        self, canal: int, imo: int, open_port_id: int, load_port_id: int,
            discharge_port_id: int, ballast_speed: float, laden_speed: float,
            operation_status: int, formula_calculation_date: datetime,
            open_date: datetime, load_sail_date: datetime,
            cargo_type: Optional[str] = None) -> Optional[CanalExpenses]:
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
        return_object = parse_canal_expenses(response_json) \
            if response_json else None

        return return_object

    def get_port_model_vessel_expenses(
        self, port_id: int, vessel_type_id: int,
            formula_calculation_date: datetime, vessel_class_id: int = 0,
            operation_status: int = 0, historical_tce: bool = False,
            estimation_status: int = 0) -> Optional[PortExpenses]:
        """Retrieves model vessel port expenses.

        Args:
            port_id
            vessel_type_id
            formula_calculation_date
            vessel_class_id
            operation_status
            historical_tce
            estimation_status

        Returns:
            The port expenses for model vessel or None if a port with given ID
            does not exist or a vessel type with the given ID number does not
            exist.
        """
        query_string: QueryString = {
            "portId": '{}'.format(port_id),
            "vesselTypeId": '{}'.format(vessel_type_id),
            "formulaCalculationDate": formula_calculation_date.isoformat(),
            "vesselClassId": '{}'.format(vessel_class_id),
            "operationStatus": '{}'.format(operation_status),
            "historicalTce": '{}'.format(historical_tce),
            "estimationStatus": '{}'.format(estimation_status)
        }

        response = self.__connection._make_post_request(
            "port-expenses/api/v1/PortModelVessel", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_port_expenses(response_json) \
            if response_json else None

        return return_object

    def get_canal_model_vessel_expenses(
        self, canal: int, open_port_id: int, load_port_id: int,
            discharge_port_id: int, operation_status: int,
            formula_calculation_date: datetime) -> Optional[CanalExpenses]:
        """Retrieves model vessel canal expenses.

        Args:
            canal
            open_port_id
            load_port_id
            discharge_port_id
            operation_status
            formula_calculation_date

        Returns:
            The canal expenses for model vessel or None if expenses can be
            provided for the given parameters.
        """
        query_string: QueryString = {
            "canal": '{}'.format(canal),
            "openPortId": '{}'.format(open_port_id),
            "loadPortId": '{}'.format(load_port_id),
            "dischargePortId": '{}'.format(discharge_port_id),
            "operationStatus": '{}'.format(operation_status),
            "formulaCalculationDate": formula_calculation_date.isoformat()
        }

        response = self.__connection._make_post_request(
            "port-expenses/api/v1/CanalModelVessel", query_string
        )
        response.raise_for_status()
        response_json = {"TotalCost": response.json()}
        return_object = parse_canal_expenses(response_json) \
            if response_json else None

        return return_object
