# noqa: D100

from datetime import datetime
from typing import cast, Optional, List, Tuple

from .. import Connection
from .._internals import QueryString
from .enums import Operation, OperationStatus, EstimationStatus,\
    ItalianAnchorageDues, VesselTypeEnum
from .models import PortExpenses, Port, VesselType
from .port_filter import PortFilter
from ._port_expenses_json import parse_port_expenses, parse_ports


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
            operation: Optional[Operation] = None,
            italian_anchorage_dues: Optional[ItalianAnchorageDues] = None,
            cargo_type: Optional[str] = None,
            operation_status: Optional[OperationStatus] = None,
            utc_date: Optional[datetime] = None,
            historical_tce: Optional[bool] = None,
            estimation_status: Optional[EstimationStatus] = None
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
            query_dict["operation"] = '{}'.format(operation.value)
        if italian_anchorage_dues is not None:
            query_dict["italianAnchorageDues"] = \
                '{}'.format(italian_anchorage_dues.value)
        if cargo_type is not None:
            query_dict["cargoType"] = '{}'.format(cargo_type)
        if operation_status is not None:
            query_dict["operationStatus"] = '{}'.format(operation_status.value)
        if utc_date is not None:
            query_dict["utcDate"] = utc_date.isoformat()
        if historical_tce is not None:
            query_dict["historicalTce"] = '{}'.format(historical_tce)
        if estimation_status is not None:
            query_dict["estimationStatus"] = \
                '{}'.format(estimation_status.value)

        query_string: QueryString = query_dict
        response = self.__connection._make_post_request(
            "port-expenses/api/v1/Port", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_port_expenses(response_json) \
            if response_json else None

        return return_object

    def get_port_model_vessel_expenses(
        self, port_id: int, vessel_type_id: int,
            formula_calculation_date: datetime, vessel_class_id: int = 0,
            operation_status: OperationStatus = OperationStatus.BALLAST,
            historical_tce: bool = False,
            estimation_status: EstimationStatus =
            EstimationStatus.PRIORITY_TO_FORMULAS) -> Optional[PortExpenses]:
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
            "operationStatus": '{}'.format(operation_status.value),
            "historicalTce": '{}'.format(historical_tce),
            "estimationStatus": '{}'.format(estimation_status.value)
        }

        response = self.__connection._make_post_request(
            "port-expenses/api/v1/PortModelVessel", query_string
        )
        response.raise_for_status()
        response_json = response.json()
        return_object = parse_port_expenses(response_json) \
            if response_json else None

        return return_object

    def get_required_formula_parameters(
        self, port_id: int, vessel_type_id: int,
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
            "portId": '{}'.format(port_id),
            "vesselTypeId": '{}'.format(vessel_type_id),
        }

        if calculation_date is not None:
            query_dict["calculationDate"] = calculation_date.isoformat()

        query_string: QueryString = query_dict
        response = self.__connection._make_post_request(
            "port-expenses/api/v1/RequiredFormulaParameters", query_string
        )
        response.raise_for_status()
        response_json = response.json()

        return cast(List[str], response_json)

    def get_vessel_types(self) -> Tuple[VesselType, ...]:
        """Retrieves all available vessel types.

        Returns:
            A tuple of all available vessel types.
        """
        vessel_types = tuple(VesselType(vessel_type.value, vessel_type.name)
                             for vessel_type in VesselTypeEnum)
        return vessel_types

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
            "date": datetime.now().isoformat()
        }

        query_string: QueryString = query_dict

        available_ports: List[Port] = []
        for vessel_type in VesselTypeEnum:
            response = self.__connection._make_get_request(
                f"port-expenses/api/v1/AvailablePorts/{vessel_type.value}",
                query_string
            )
            response.raise_for_status()
            response_json = response.json()
            available_ports += parse_ports(response_json)

        port_filter = port_filter or PortFilter()

        return tuple(port_filter._apply(available_ports))
