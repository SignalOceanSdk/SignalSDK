import datetime
import json
from datetime import date
from unittest.mock import MagicMock

import pandas as pd
from freezegun import freeze_time
from pandas.testing import assert_frame_equal

from signal_ocean.port_congestion import PortCongestion
from signal_ocean.port_congestion.models import PortCongestionQueryResponse
from signal_ocean.util.parsing_helpers import parse_model

_mock_voyages = pd.read_csv("tests/port_congestion/Data/mock_voyages.csv")
_mock_events = pd.read_csv(
    "tests/port_congestion/Data/mock_events.csv",
    parse_dates=["arrival_date", "sailing_date", "event_date"],
)
_mock_events_details = pd.read_csv(
    "tests/port_congestion/Data/mock_events_details.csv",
    parse_dates=[
        "arrival_date",
        "start_time_of_operation",
        "end_time_of_operation",
        "sailing_date",
    ],
)
_mock_geos = pd.read_csv("tests/port_congestion/Data/mock_geos.csv")
_mock_vessels_congestion_data = pd.read_csv(
    "tests/port_congestion/Data/mock_vessels_congestions_data.csv",
    parse_dates=[
        "waiting_time_start",
        "waiting_time_end",
        "operating_time_start",
        "operating_time_end",
        "day_date",
        "arrival_date",
    ],
)
_mock_number_of_vessels_over_time = pd.read_csv(
    "tests/port_congestion/Data/mock_number_of_vessels_over_time.csv",
    parse_dates=["date"],
)
_mock_waiting_time_over_time = pd.read_csv(
    "tests/port_congestion/Data/mock_waiting_time_over_time.csv",
    parse_dates=["date"],
)
_mock_live_port_congestion = pd.read_csv(
    "tests/port_congestion/Data/mock_live_port_congestion.csv",
    parse_dates=[
        "waiting_time_start",
        "waiting_time_end",
        "operating_time_start",
        "operating_time_end",
        "day_date",
        "arrival_date",
    ],
)

with open("tests/port_congestion/Data/mock_port_congestion_api_response.json") as fp:
    _mock_port_congestion_api_response = json.load(fp)

_port_congestion = PortCongestion()

_port_congestion._get_voyages_data = MagicMock(
    return_value=(
        _mock_voyages,
        _mock_events,
        _mock_events_details,
        _mock_geos,
    )
)

_parsed_congestion_api_mock_response = parse_model(_mock_port_congestion_api_response, PortCongestionQueryResponse)
_port_congestion._port_congestion_api.query_port_congestion = MagicMock(
    return_value=_parsed_congestion_api_mock_response.time_series
)


@freeze_time("2022-03-03")
def test_preprocess_voyages_data():
    (
        voyages_df,
        events_df,
        events_details_df,
        geos_df,
    ) = _port_congestion._get_voyages_data(date(2022, 1, 2), 70)

    vessels_congestion_data = _port_congestion._preprocess_voyages_data(
        voyages_df, events_df, events_details_df, geos_df, date(2022, 2, 2)
    )

    assert not assert_frame_equal(
        _mock_vessels_congestion_data, vessels_congestion_data
    )


@freeze_time("2022-03-03")
def test_number_of_vessels_over_time():
    number_of_vessels_over_time = (
        _port_congestion._calculate_number_of_vessels_over_time(
            _mock_vessels_congestion_data
        )
    )

    assert not assert_frame_equal(
        _mock_number_of_vessels_over_time, number_of_vessels_over_time
    )


def test_waiting_time_over_time():
    vessel_class_id = 70
    date_from = datetime.datetime(2022, 3, 3)
    waiting_df = _mock_vessels_congestion_data.loc[_mock_vessels_congestion_data["mode"] == "Waiting"]
    ports = waiting_df["port_name_geos"].unique().tolist()
    level_0_areas = waiting_df["area_name_level0_geos"].unique().tolist()

    waiting_time_over_time = (
        _port_congestion._get_waiting_time_over_time(
            congestion_start_date=date_from,
            vessel_class_id=vessel_class_id,
            ports=ports,
            areas=level_0_areas,
        )
    )

    assert not assert_frame_equal(
        _mock_waiting_time_over_time, waiting_time_over_time
    )


@freeze_time("2022-03-03")
def test_get_live_port_congestion():
    live_port_congestion = _port_congestion._calculate_live_port_congestion(
        _mock_vessels_congestion_data
    )

    assert not assert_frame_equal(
        _mock_live_port_congestion, live_port_congestion
    )
