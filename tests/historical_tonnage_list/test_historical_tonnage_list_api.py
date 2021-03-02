from datetime import date, time
from unittest.mock import MagicMock, call

from signal_ocean.historical_tonnage_list import HistoricalTonnageListAPI

from ..builders import create_port, create_vessel_class


def test_passes_provided_parameters_to_query_string():
    connection = MagicMock()
    api = HistoricalTonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port, vessel_class, 3, date(2020, 5, 1), date(2020, 6, 1), time(6)
    )

    connection._make_get_request.assert_called_with(
        "htl-api/historical-tonnage-list/",
        {
            "loadingPort": port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": 3,
            "startDate": "2020-05-01",
            "endDate": "2020-06-01",
            "time": "06:00",
        },
    )


def test_handles_optional_parameters():
    connection = MagicMock()
    api = HistoricalTonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port,
        vessel_class,
        laycan_end_in_days=None,
        start_date=None,
        end_date=None,
        time=None,
    )

    connection._make_get_request.assert_called_with(
        "htl-api/historical-tonnage-list/",
        {
            "loadingPort": port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": None,
            "startDate": None,
            "endDate": None,
            "time": None,
        },
    )


def test_splits_long_date_ranges_into_multiple_calls():
    connection = MagicMock()
    api = HistoricalTonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port, vessel_class, None, date(2020, 1, 1), date(2021, 6, 1)
    )

    connection._make_get_request.assert_has_calls(
        [
            call(
                "htl-api/historical-tonnage-list/",
                {
                    "loadingPort": port.id,
                    "vesselClass": vessel_class.id,
                    "laycanEndInDays": None,
                    "startDate": "2020-01-01",
                    "endDate": "2020-12-30",
                    "time": None,
                },
            ),
            call(
                "htl-api/historical-tonnage-list/",
                {
                    "loadingPort": port.id,
                    "vesselClass": vessel_class.id,
                    "laycanEndInDays": None,
                    "startDate": "2020-12-31",
                    "endDate": "2021-06-01",
                    "time": None,
                },
            ),
        ],
        any_order=True
    )
