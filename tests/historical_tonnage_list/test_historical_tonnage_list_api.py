from datetime import date, time
from unittest.mock import patch, ANY

from signal_ocean.historical_tonnage_list import HistoricalTonnageListAPI

from ..builders import create_port, create_vessel_class


def test_passes_provided_parameters_to_query_string():
    api = HistoricalTonnageListAPI()
    port = create_port()
    vessel_class = create_vessel_class()

    with patch('requests.get') as requests_get:
        api.get_historical_tonnage_list(
            port,
            vessel_class,
            3,
            date(2020, 5, 1),
            date(2020, 6, 1),
            time(6))

        requests_get.assert_called_with(
            ANY,
            params={
                'loadingPort': port.id,
                'vesselClass': vessel_class.id,
                'laycanEndInDays': 3,
                'startDate': '2020-05-01',
                'endDate': '2020-06-01',
                'time': '06:00'
            },
            headers=ANY)


def test_handles_optional_parameters():
    api = HistoricalTonnageListAPI()
    port = create_port()
    vessel_class = create_vessel_class()

    with patch('requests.get') as requests_get:
        api.get_historical_tonnage_list(
            port,
            vessel_class,
            laycan_end_in_days=None,
            start_date=None,
            end_date=None,
            time=None)

        requests_get.assert_called_with(
            ANY,
            params={
                'loadingPort': port.id,
                'vesselClass': vessel_class.id,
                'laycanEndInDays': None,
                'startDate': None,
                'endDate': None,
                'time': None
            },
            headers=ANY)
