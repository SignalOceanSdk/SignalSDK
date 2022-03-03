from datetime import date, datetime, timezone
from typing import Tuple, List
from unittest.mock import MagicMock
from urllib.parse import urljoin

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import json

from signal_ocean import Connection
from signal_ocean.port_congestion import PortCongestion
from signal_ocean.voyages.models import (
    Voyage,
    VoyageEvent,
    VoyageEventDetail,
    VoyageGeo,
    VoyagesFlat,
)
from signal_ocean.port_congestion.models import (
    LiveCongestion,
    NumberOfVesselsOverTime,
    WaitingTimeOverTime,
    VesselsCongestionData,
)


class NewDate(date):
    @classmethod
    def today(cls):
        return cls(2022, 3, 3)


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

_port_congestion = PortCongestion()

_port_congestion._get_voyages_data = MagicMock(
    return_value=(
        _mock_voyages,
        _mock_events,
        _mock_events_details,
        _mock_geos,
    )
)


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
    waiting_time_over_time = (
        _port_congestion._calculate_waiting_time_over_time(
            _mock_vessels_congestion_data
        )
    )

    assert not assert_frame_equal(
        _mock_waiting_time_over_time, waiting_time_over_time
    )


def test_get_live_port_congestion():
    live_port_congestion = _port_congestion._calculate_live_port_congestion(
        _mock_vessels_congestion_data
    )

    assert not assert_frame_equal(
        _mock_live_port_congestion, live_port_congestion
    )
