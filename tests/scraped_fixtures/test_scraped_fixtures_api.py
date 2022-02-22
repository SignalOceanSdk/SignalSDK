from decimal import Decimal
from unittest.mock import patch, MagicMock, ANY
from typing import Tuple
from datetime import datetime

import requests
from signal_ocean import Connection

import pytest
from typing import Tuple, List


from signal_ocean.scraped_fixtures import ScrapedFixturesAPI, ScrapedFixture

example_request_1 ={
                    "ReceivedDateFrom": datetime(2022,1,1),
                    "ReceivedDateTo": datetime(2022,1,4),
                    "VesselType": 1
                   }

sf1 = {
    "FixtureID": 71338679,
    "MessageID": 20811043,
    "UpdatedDate": "2022-01-03T00:53:54",
    "ReceivedDate": "2022-01-03T00:52:35",
    "IMO": 9243318,
    "VesselClassID": 86,
    "OpenGeoID": 3153,
    "OpenTaxonomyID": 2,
    "OpenDate": "2022-01-03",
    "CharterTypeID": 0,
    "FixtureStatusID": 0,
    "IsOwnersOption": False,
    "IsCOA": False
}
sf2 = {
    "FixtureID": 71338680,
    "MessageID": 20811043,
    "UpdatedDate": "2022-01-03T00:53:54",
    "ReceivedDate": "2022-01-03T00:52:35",
    "IMO": 9412995,
    "VesselClassID": 86,
    "OpenGeoID": 3153,
    "OpenTaxonomyID": 2,
    "OpenDate": "2022-01-05",
    "CharterTypeID": 0,
    "FixtureStatusID": 0,
    "IsOwnersOption": False,
    "IsCOA": False
}


sf_ras_tanura_2 = ScrapedFixture(
    fixture_id=71339469,
    message_id=20813261,
    updated_date= datetime.fromisoformat("2022-01-03T02:51:49"),
    received_date=datetime.fromisoformat("2022-01-03T02:51:08"),
    imo=9383869,
    vessel_class_id=86,
    laycan_from=datetime.fromisoformat("2022-01-05T00:00:00"),
    laycan_to=datetime.fromisoformat("2022-01-05T00:00:00"),
    load_geo_id=3778,
    load_taxonomy_id=2,
    discharge_geo_id=24778,
    discharge_taxonomy_id=4,
    charterer_id=1436,
    cargo_type_id=16,
    cargo_group_id=130000,
    quantity=90000.0,
    quantity_buffer=0.0,
    quantity_from=90000.0,
    quantity_to=90000.0,
    charterer_type_id=0,
    is_owners_option=False,
    is_coa=False,
)

sf_ras_tanura_1 = ScrapedFixture(
    fixture_id=71339456,
    message_id=20813261,
    updated_date= datetime.fromisoformat("2022-01-03T02:51:53"),
    received_date=datetime.fromisoformat("2022-01-03T02:51:08"),
    imo=9486934,
    vessel_class_id=86,
    laycan_from=datetime.fromisoformat("2022-01-01T00:00:00"),
    laycan_to=datetime.fromisoformat("2022-01-03T00:00:00"),
    load_geo_id=3778,
    load_taxonomy_id=2,
    discharge_geo_id=24778,
    discharge_taxonomy_id=4,
    charterer_id=1436,
    cargo_type_id=16,
    cargo_group_id=130000,
    quantity=90000.0,
    quantity_buffer=0.0,
    quantity_from=90000.0,
    quantity_to=90000.0,
    charterer_type_id=0,
    is_owners_option=False,
    is_coa=True,
)


def create_sf_api(
    response_data: List = None,
) -> Tuple[ScrapedFixturesAPI, MagicMock]:
    connection = Connection("", "")
    response = MagicMock()
    response.json.return_value = response_data
    
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = ScrapedFixturesAPI(connection)
    return api, mocked_make_request



@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type",
    [
        (datetime(2022,1,1), datetime(2022,1,4), 1),
        
    ],
)
def test_get_fixtures(received_date_from,received_date_to,vessel_type):

    mock_response = (
        sf1,
        sf2,
    )
    # api, connection = create_sf_api(mock_response)
    api = ScrapedFixturesAPI(Connection("5ee27a085a1a40ac8cc84309cab3957e"))

    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        )

    assert len(results) == 1391

    

@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type, port_id",
    [
        (datetime(2022,1,1), datetime(2022,1,6), 1, 3778),
        
    ],
)
def test_get_fixtures_by_port(received_date_from, received_date_to, vessel_type, port_id):

    mock_response = [
        sf_ras_tanura_1,
        sf_ras_tanura_2,
    ]
    # api, connection = create_sf_api(mock_response)
    api = ScrapedFixturesAPI(Connection("5ee27a085a1a40ac8cc84309cab3957e"))

    results = api.get_fixtures_by_port(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        port_id= port_id
        )

    assert (len(results)) == 10


