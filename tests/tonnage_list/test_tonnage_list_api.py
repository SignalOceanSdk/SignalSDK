from datetime import date, time
from unittest.mock import MagicMock, call

from signal_ocean.tonnage_list import TonnageListAPI
from signal_ocean.tonnage_list.models import DateRange

from .builders import create_port, create_vessel_class


def test_passes_provided_parameters_to_query_string() -> None:
    connection = MagicMock()
    api = TonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port, vessel_class, 3, DateRange(date(2020, 5, 1), date(2020, 6, 1))
    )

    connection._make_get_request.assert_called_with(
        "htl-api/historical-tonnage-list/",
        {
            "loadingPort": port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": 3,
            "startDate": "2020-05-01",
            "endDate": "2020-06-01",
        },
    )


def test_handles_optional_parameters() -> None:
    connection = MagicMock()
    api = TonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port, vessel_class, laycan_end_in_days=None, date_range=None,
    )

    connection._make_get_request.assert_called_with(
        "htl-api/historical-tonnage-list/",
        {
            "loadingPort": port.id,
            "vesselClass": vessel_class.id,
            "laycanEndInDays": None,
            "startDate": None,
            "endDate": None,
        },
    )


def test_splits_long_date_ranges_into_multiple_calls() -> None:
    connection = MagicMock()
    api = TonnageListAPI(connection)
    port = create_port()
    vessel_class = create_vessel_class()

    api.get_historical_tonnage_list(
        port, vessel_class, None, DateRange(date(2020, 1, 1), date(2021, 6, 1))
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
                },
            ),
        ],
        any_order=True,
    )
