from unittest.mock import MagicMock
from signal_ocean.voyages import VoyagesAPI
from signal_ocean.voyages.models import VesselClass
from signal_ocean import Connection

__mock_vessel_classes_response = [{
    "VesselClassID": 60,
    "VesselClassName": "VLGC",
    "VesselTypeID": 6,
    "VesselType": "LPG"
}, {
    "VesselClassID": 61,
    "VesselClassName": "Midsize/LGC",
    "VesselTypeID": 6,
    "VesselType": "LPG"
}, {
    "VesselClassID": 69,
    "VesselClassName": "VLOC",
    "VesselTypeID": 3,
    "VesselType": "Dry"
}, {
    "VesselClassID": 70,
    "VesselClassName": "Capesize",
    "VesselTypeID": 3,
    "VesselType": "Dry"
}, {
    "VesselClassID": 72,
    "VesselClassName": "Post Panamax",
    "VesselTypeID": 3,
    "VesselType": "Dry"
}, {
    "VesselClassID": 74,
    "VesselClassName": "Panamax",
    "VesselTypeID": 3,
    "VesselType": "Dry"
}, {
    "VesselClassID": 84,
    "VesselClassName": "VLCC",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselClassID": 85,
    "VesselClassName": "Suezmax",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselClassID": 86,
    "VesselClassName": "Aframax",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselClassID": 87,
    "VesselClassName": "Panamax",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselClassID": 88,
    "VesselClassName": "MR2",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}, {
    "VesselClassID": 89,
    "VesselClassName": "MR1",
    "VesselTypeID": 1,
    "VesselType": "Tanker"
}]


__mock_vessel_classes_response_model = [VesselClass(
    vessel_class_id= 60,
    vessel_class_name= "VLGC",
    vessel_type_id= 6,
    vessel_type= "LPG"
), VesselClass(
    vessel_class_id= 61,
    vessel_class_name= "Midsize/LGC",
    vessel_type_id= 6,
    vessel_type= "LPG"
), VesselClass(
    vessel_class_id= 69,
    vessel_class_name= "VLOC",
    vessel_type_id= 3,
    vessel_type= "Dry"
), VesselClass(
    vessel_class_id= 70,
    vessel_class_name= "Capesize",
    vessel_type_id= 3,
    vessel_type= "Dry"
), VesselClass(
    vessel_class_id= 72,
    vessel_class_name= "Post Panamax",
    vessel_type_id= 3,
    vessel_type= "Dry"
), VesselClass(
    vessel_class_id= 74,
    vessel_class_name= "Panamax",
    vessel_type_id= 3,
    vessel_type= "Dry"
), VesselClass(
    vessel_class_id= 84,
    vessel_class_name= "VLCC",
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselClass(
    vessel_class_id= 85,
    vessel_class_name= "Suezmax",
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselClass(
    vessel_class_id= 86,
    vessel_class_name= "Aframax",
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselClass(
    vessel_class_id= 87,
    vessel_class_name= "Panamax",
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselClass(
    vessel_class_id= 88,
    vessel_class_name= "MR2",
    vessel_type_id= 1,
    vessel_type= "Tanker"
), VesselClass(
    vessel_class_id= 89,
    vessel_class_name= "MR1",
    vessel_type_id= 1,
    vessel_type= "Tanker"
)]

def test_get_vessel_classes():
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = __mock_vessel_classes_response
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VoyagesAPI(connection)

    vessel_classes = api.get_vessel_classes()

    assert [v.vessel_class_id for v in vessel_classes] == [vessel_class.vessel_class_id for vessel_class in __mock_vessel_classes_response_model]