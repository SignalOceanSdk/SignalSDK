from unittest.mock import MagicMock
from signal_ocean.voyages import VoyagesAPI
from signal_ocean.voyages import VesselType
from signal_ocean import Connection

__mock_vessel_types_response_model = [
VesselType(
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselType(
    vessel_type_id= 3,
    vessel_type= "Dry"
), VesselType(
    vessel_type_id= 6,
    vessel_type= "LPG"
)]

__mock_vessel_types_response = [{
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselTypeID": 3,
    "VesselType": "Dry"
}, {
    "VesselTypeID": 6,
    "VesselType": "LPG"
}]


def test_get_vessel_types():
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = __mock_vessel_types_response
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesAPI(connection)

    vessel_types = api.get_vessel_types()

    assert [v.vessel_type_id for v in vessel_types] == [vessel_type.vessel_type_id for vessel_type in __mock_vessel_types_response_model]