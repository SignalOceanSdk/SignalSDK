# noqa: D100

from datetime import datetime
from typing import cast, Optional, List

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
        self, imo: int, port_id: int, group_id: int = 1,
            vessel_type_id: Optional[int] = None,
            estimated_time_of_berth: Optional[datetime] = None,
            estimated_time_of_sail: Optional[datetime] = None,
            operation: Optional[int] = None,
            italian_anchorage_dues: Optional[int] = None,
            cargo_type: Optional[str] = None,
            operation_status: Optional[int] = None,
            utc_date: Optional[datetime] = None,
            historical_tce: Optional[bool] = None,
            estimation_status: Optional[int] = None
    ) -> Optional[PortExpenses]:
        """Retrieves port expenses.

        Args:
            imo: The vessel's IMO number.
            port_id: ID of the port to retrieve the expenses for.
            group_id: Group ID.
            vessel_type_id: Vessel type ID.
            estimated_time_of_berth: Estimated time of berth.
            estimated_time_of_sail: Estimated time of sail.
            operation: Operation type.
            italian_anchorage_dues: Italian anchorage dues.
            cargo_type: Cargo type.
            operation_status: Operation status.
            utc_date: UTC date.
            historical_tce: Flag for Historical TCE.
            estimation_status: Estimation status.

        Returns:
            The port expenses or None if a port with given ID does not exist or
            a vessel with the given IMO number does not exist.
        """
        query_dict = {
            "imo": '{}'.format(imo),
            "portId": '{}'.format(port_id),
            "groupId": '{}'.format(group_id)
        }

        if vessel_type_id is not None:
            query_dict["vesselTypeId"] = '{}'.format(vessel_type_id)
        if estimated_time_of_berth is not None:
            query_dict["estimatedTimeOfBerth"] = \
                estimated_time_of_berth.isoformat()
        if estimated_time_of_sail is not None:
            query_dict["estimatedTimeOfSail"] = \
                estimated_time_of_sail.isoformat()
        if operation is not None:
            query_dict["operation"] = '{}'.format(operation)
        if italian_anchorage_dues is not None:
            query_dict["italianAnchorageDues"] = \
                '{}'.format(italian_anchorage_dues)
        if cargo_type is not None:
            query_dict["cargoType"] = '{}'.format(cargo_type)
        if operation_status is not None:
            query_dict["operationStatus"] = '{}'.format(operation_status)
        if utc_date is not None:
            query_dict["utcDate"] = utc_date.isoformat()
        if historical_tce is not None:
            query_dict["historicalTce"] = '{}'.format(historical_tce)
        if estimation_status is not None:
            query_dict["estimationStatus"] = '{}'.format(estimation_status)

        query_string: QueryString = query_dict
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
            canal: ID of the canal to retrieve the expenses for.
            imo: The vessel's IMO number.
            open_port_id: Open port ID.
            load_port_id: Load port ID.
            discharge_port_id: Discharge port ID.
            ballast_speed: Ballast speed.
            laden_speed: Laden speed.
            operation_status: Operation status.
            formula_calculation_date: Formula calculation date
            open_date: Open date.
            load_sail_date: Load sail date.
            cargo_type: Cargo type.

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
            port_id: ID of the port to retrieve the expenses for.
            vessel_type_id: Vessel type ID.
            formula_calculation_date: Formula calculation date.
            vessel_class_id: Vessel class ID.
            operation_status: Operation status.
            historical_tce: Flag for historical TCE.
            estimation_status: Estimation status.

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
            canal: ID of the canal to retrieve the expenses for.
            open_port_id: Open port ID.
            load_port_id: Load port ID.
            discharge_port_id: Discharge port ID.
            operation_status: Operation status.
            formula_calculation_date: Formula calculation date.

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

    def get_required_formula_parameters(
        self, port_id: int, vessel_type_id: Optional[int] = None,
            calculation_date: Optional[datetime] = None
    ) -> List[str]:
        """Retrieves required formula parameters.

        Args:
            port_id: ID of the port to retrieve the expenses for.
            vessel_type_id: Vessel type ID.
            calculation_date: Calculation date.

        Returns:
            List of required port expenses formula calculation parameters.
        """
        query_dict = {
            "portId": '{}'.format(port_id)
        }

        if vessel_type_id is not None:
            query_dict["vesselTypeId"] = '{}'.format(vessel_type_id)
        if calculation_date is not None:
            query_dict["calculationDate"] = calculation_date.isoformat()

        query_string: QueryString = query_dict
        response = self.__connection._make_post_request(
            "port-expenses/api/v1/RequiredFormulaParameters", query_string
        )
        response.raise_for_status()
        response_json = response.json()

        return cast(List[str], response_json)
