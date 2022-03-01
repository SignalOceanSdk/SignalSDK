from unittest.mock import MagicMock
from signal_ocean.voyages import VoyagesAPI
from signal_ocean.voyages import Vessel, VesselFilter
from signal_ocean import Connection

__mock_vessels_response_model = [
Vessel(
    imo= 7347665,
    vessel_name= "Mitra"
)]

__mock_vessels_response = [{
    "IMO": 7347665,
    "VesselName": "Mitra"
}]


def test_get_vessels():
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = __mock_vessels_response
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesAPI(connection)

    vessels = api.get_imos(VesselFilter("Mit"))

    assert [v.imo for v in vessels] == [vessel.imo for vessel in __mock_vessels_response_model]