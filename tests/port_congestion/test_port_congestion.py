from datetime import date, datetime, timezone
from typing import Tuple, List
from unittest.mock import MagicMock
from urllib.parse import urljoin

import pytest
import pandas as pd

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

_mock_voyages = pd.read_json("mock_voyages.json", orient="split")
_mock_events = pd.read_json("mock_events.json", orient="split")
_mock_events_details = pd.read_json("mock_events_details.json", orient="split")
_mock_geos = pd.read_json("mock_geos.json", orient="split")
_mock_vessels_congestion_data = pd.read_json("mock_vessels_congestion_data.json", orient="split")

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

    (voyages_df,
    events_df,
    events_details_df,
    geos_df) = _port_congestion._get_voyages_data(date(2022, 1, 2), 70)

    vessels_congestion_data = (
        _port_congestion
        ._preprocess_voyages_data(
            voyages_df,
            events_df,
            events_details_df,
            geos_df,
            date(2022, 2, 2)
        )
    )
    
    assert vessels_congestion_data == _mock_vessels_congestion_data