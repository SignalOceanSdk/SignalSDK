from datetime import datetime

from unittest.mock import MagicMock

import pytest

from signal_ocean.port_expenses import PortExpensesAPI, PortExpenses, \
    CanalExpenses


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
     datetime(2020, 2, 27, 17, 48, 11), 1, 1, "test", 1,
     datetime(2020, 2, 27, 17, 48, 11), True, 1)
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
            "operation": '{}'.format(operation),
            "italianAnchorageDues": '{}'.format(italian_anchorage_dues),
            "cargoType": '{}'.format(cargo_type),
            "operationStatus": '{}'.format(operation_status),
            "utcDate": utc_date.isoformat(),
            "historicalTce": '{}'.format(historical_tce),
            "estimationStatus": '{}'.format(estimation_status)
        },
    )


@pytest.mark.parametrize('canal, imo, open_port_id, load_port_id, '
                         'discharge_port_id, ballast_speed, laden_speed, '
                         'operation_status, formula_calculation_date, '
                         'open_date, load_sail_date, cargo_type', [
    (1, 9867621, 3773, 3360, 3794, 12.0, 12.5, 0,
     datetime(2020, 2, 27, 17, 48, 11), datetime(1, 1, 1, 0, 0, 0),
     datetime(1, 1, 1, 0, 0, 0), "Product")
])
def test_get_canal_expenses(canal, imo, open_port_id, load_port_id,
                            discharge_port_id, ballast_speed, laden_speed,
                            operation_status, formula_calculation_date,
                            open_date, load_sail_date, cargo_type):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    canal_expenses = api.get_canal_expenses(canal, imo, open_port_id,
                                            load_port_id, discharge_port_id,
                                            ballast_speed, laden_speed,
                                            operation_status,
                                            formula_calculation_date,
                                            open_date, load_sail_date,
                                            cargo_type)

    assert type(canal_expenses) is CanalExpenses

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/Canal",
        {
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


@pytest.mark.parametrize('canal, open_port_id, load_port_id, '
                         'discharge_port_id, operation_status, '
                         'formula_calculation_date', [
    (2, 3758, 3758, 3617, 1, datetime(2018, 1, 8, 5, 26, 36)),
    (1, 3773, 3360, 3794, 1, datetime(2020, 2, 27, 17, 48, 11))
])
def test_get_canal_model_vessel_expenses(canal, open_port_id, load_port_id,
                                         discharge_port_id, operation_status,
                                         formula_calculation_date):
    connection = MagicMock()
    api = PortExpensesAPI(connection)

    canal_expenses = api.get_canal_model_vessel_expenses(canal, open_port_id,
                                                         load_port_id,
                                                         discharge_port_id,
                                                         operation_status,
                                                         formula_calculation_date)

    assert type(canal_expenses) is CanalExpenses

    connection._make_post_request.assert_called_with(
        "port-expenses/api/v1/CanalModelVessel",
        {
            "canal": '{}'.format(canal),
            "openPortId": '{}'.format(open_port_id),
            "loadPortId": '{}'.format(load_port_id),
            "dischargePortId": '{}'.format(discharge_port_id),
            "operationStatus": '{}'.format(operation_status),
            "formulaCalculationDate": formula_calculation_date.isoformat()
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