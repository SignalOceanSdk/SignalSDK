from datetime import datetime

from unittest.mock import MagicMock

import pytest

from signal_ocean.market_rates import MarketRatesAPI, MarketRate, \
    Route, VesselClass
from signal_ocean.market_rates.vessel_classes import VESSEL_CLASSES


@pytest.mark.parametrize('start_date, route_id, vessel_class_id, end_date, '
                         'is_clean', [
                             (datetime(2020, 2, 27), "R54", None, None, None),
                             (datetime(2020, 2, 27), None, 77, None, None),
                             (datetime(2020, 2, 27), "R54", 77,
                              datetime(2020, 2, 28), None),
                             (datetime(2020, 2, 27), "R54", 77,
                              datetime(2020, 2, 28), True)
                         ])
def test_get_market_rates(start_date, route_id, vessel_class_id, end_date,
                          is_clean):
    connection = MagicMock()
    api = MarketRatesAPI(connection)

    mr_object = api.get_market_rates(start_date, route_id, vessel_class_id,
                                     end_date, is_clean)

    assert isinstance(mr_object, tuple)
    assert all([isinstance(mr, MarketRate) for mr in mr_object])

    connection._make_get_request.assert_called_with(
        "market-rates/api/v1/market_rates",
        {
            "start_date": start_date.isoformat(),
            "route_id": '{}'.format(route_id),
            "vessel_class_id": '{}'.format(vessel_class_id),
            "end_date": end_date.isoformat(),
            "is_clean": is_clean.isoformat()
        }
    )


@pytest.mark.parametrize('vessel_class_id', [
                             None, 77, 86
                         ])
def test_get_routes(vessel_class_id):
    connection = MagicMock()
    api = MarketRatesAPI(connection)

    r_object = api.get_routes(vessel_class_id)

    assert isinstance(r_object, tuple)
    assert all([isinstance(r, Route) for r in r_object])

    if vessel_class_id:
        connection._make_get_request.assert_called_with(
            f"market-rates/api/v1/routes/{vessel_class_id}"
        )
    else:
        connection._make_get_request.assert_called_with(
            "market-rates/api/v1/routes"
        )


def test_get_vessel_classes():
    connection = MagicMock()
    api = MarketRatesAPI(connection)

    vessel_classes = api.get_vessel_classes()

    assert vessel_classes == tuple(
        VesselClass(vessel_class["id"], vessel_class["vessel_type_id"],
                    vessel_class["from_size"], vessel_class["to_size"],
                    vessel_class["vessel_type"], vessel_class["defining_size"],
                    vessel_class["size"])
        for vessel_class in VESSEL_CLASSES)
