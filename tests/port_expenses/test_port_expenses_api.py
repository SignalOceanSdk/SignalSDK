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