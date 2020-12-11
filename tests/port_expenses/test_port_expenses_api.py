from datetime import datetime

from unittest.mock import MagicMock

import pytest

from signal_ocean.port_expenses import PortExpensesAPI, PortExpenses, \
    Operation, OperationStatus, ItalianAnchorageDues, EstimationStatus


@pytest.mark.parametrize('imo, port_id', [
    (9867621, 3153), (9303144, 3154), (9382700, 3155)
])
def test_get_port_expenses(imo, port_id):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    pe_object = api.get_port_expenses(imo, port_id)

    assert type(pe_object) is PortExpenses

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/Port",
        {
            "imo": '{}'.format(imo),
            "portId": '{}'.format(port_id),
            "groupId": "1"
        },
    )


@pytest.mark.parametrize('imo, port_id, group_id, vessel_type_id, '
                         'estimated_time_of_berth, estimated_time_of_sail, '
                         'operation, italian_anchorage_dues, cargo_type, '
                         'operation_status, utc_date, historical_tce, '
                         'estimation_status', [
    (9867621, 3153, 1, 3, datetime(2020, 2, 27, 17, 48, 11),
     datetime(2020, 2, 27, 17, 48, 11), Operation.DISCHARGE,
     ItalianAnchorageDues.MONTHLY, "test", OperationStatus.LADEN,
     datetime(2020, 2, 27, 17, 48, 11), True,
     EstimationStatus.PRIORITY_TO_ESTIMATES)
])
def test_get_port_expenses_with_optional_params(imo, port_id, group_id,
                                                vessel_type_id,
                                                estimated_time_of_berth,
                                                estimated_time_of_sail,
                                                operation,
                                                italian_anchorage_dues,
                                                cargo_type, operation_status,
                                                utc_date, historical_tce,
                                                estimation_status):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    pe_object = api.get_port_expenses(imo, port_id, group_id,
                                      vessel_type_id,
                                      estimated_time_of_berth,
                                      estimated_time_of_sail,
                                      operation,
                                      italian_anchorage_dues,
                                      cargo_type, operation_status,
                                      utc_date, historical_tce,
                                      estimation_status)

    assert type(pe_object) is PortExpenses

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/Port",
        {
            "imo": '{}'.format(imo),
            "portId": '{}'.format(port_id),
            "groupId": "1",
            "vesselTypeId": '{}'.format(vessel_type_id),
            "estimatedTimeOfBerth": estimated_time_of_berth.isoformat(),
            "estimatedTimeOfSail": estimated_time_of_sail.isoformat(),
            "operation": '{}'.format(operation.value),
            "italianAnchorageDues": '{}'.format(italian_anchorage_dues.value),
            "cargoType": '{}'.format(cargo_type),
            "operationStatus": '{}'.format(operation_status.value),
            "utcDate": utc_date.isoformat(),
            "historicalTce": '{}'.format(historical_tce),
            "estimationStatus": '{}'.format(estimation_status.value)
        },
    )


@pytest.mark.parametrize('port_id, vessel_type_id, '
                         'formula_calculation_date', [
    (3689, 3, datetime(2020, 6, 8, 0, 0, 0)),
    (3153, 4, datetime(2020, 6, 12, 0, 0, 0)),
    (3324, 5, datetime(2020, 3, 8, 0, 0, 0))
])
def test_get_port_model_vessel_expenses(port_id, vessel_type_id,
                                        formula_calculation_date):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    pe_object = api.get_port_model_vessel_expenses(port_id, vessel_type_id,
                                                   formula_calculation_date)

    assert type(pe_object) is PortExpenses

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/PortModelVessel",
        {
            "portId": '{}'.format(port_id),
            "vesselTypeId": '{}'.format(vessel_type_id),
            "formulaCalculationDate": formula_calculation_date.isoformat(),
            'vesselClassId': '0',
            'operationStatus': '0',
            'historicalTce': 'False',
            'estimationStatus': '0'
        },
    )


@pytest.mark.parametrize('port_id, vessel_type_id, calculation_date', [
    (3153, None, None), (3153, 3, None),
    (3153, 3, datetime(2020, 2, 27, 17, 48, 11))
])
def test_get_required_formula_parameters(port_id, vessel_type_id,
                                         calculation_date):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    api.get_required_formula_parameters(port_id, vessel_type_id,
                                        calculation_date)

    query_params = {
        "portId": '{}'.format(port_id)
    }
    if vessel_type_id is not None:
        query_params["vesselTypeId"] = '{}'.format(vessel_type_id)
    if calculation_date is not None:
        query_params["calculationDate"] = calculation_date.isoformat()

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/RequiredFormulaParameters",
        query_params,
    )