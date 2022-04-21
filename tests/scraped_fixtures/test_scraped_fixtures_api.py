from decimal import Decimal
from pickle import NONE
from unittest.mock import patch, MagicMock, ANY
from typing import Tuple
from datetime import datetime, date, timezone


import requests


from signal_ocean import Connection

import pytest
from typing import Tuple, List


from signal_ocean.scraped_fixtures import ScrapedFixturesAPI, ScrapedFixture

example_request_1 = {
    "ReceivedDateFrom": datetime(2022, 1, 1),
    "ReceivedDateTo": datetime(2022, 1, 4),
    "VesselType": 1,
}

deleted_fixtures = {"FixtureID": 85374825, "IsDeleted": True}

deleted_fixtures_model = ScrapedFixture(fixture_id=85374825, is_deleted=True)

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
    "IsCOA": False,
}
sf_1_model = ScrapedFixture(
    fixture_id=71338679,
    message_id=20811043,
    updated_date=datetime.fromisoformat("2022-01-03T00:53:54").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T00:52:35").replace(
        tzinfo=timezone.utc
    ),
    imo=9243318,
    vessel_class_id=86,
    open_geo_id=3153,
    open_taxonomy_id=2,
    open_date=datetime.fromisoformat("2022-01-03T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    charter_type_id=0,
    fixture_status_id=0,
    is_owners_option=False,
    is_coa=False,
)
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
    "IsCOA": False,
}
sf_2_model = ScrapedFixture(
    fixture_id=71338680,
    message_id=20811043,
    updated_date=datetime.fromisoformat("2022-01-03T00:53:54").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T00:52:35").replace(
        tzinfo=timezone.utc
    ),
    imo=9412995,
    vessel_class_id=86,
    open_geo_id=3153,
    open_taxonomy_id=2,
    open_date=datetime.fromisoformat("2022-01-05T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    charter_type_id=0,
    fixture_status_id=0,
    is_owners_option=False,
    is_coa=False,
)

rt_sf1 = {
    "FixtureID": 71338680,
    "MessageID": 20811043,
    "UpdatedDate": "2022-01-03T00:53:54",
    "ReceivedDate": "2022-01-03T00:52:35",
    "IMO": 9412995,
    "VesselClassID": 86,
    "OpenGeoID": 3153,
    "LoadGeoID": 3778,
    "OpenTaxonomyID": 2,
    "OpenDate": "2022-01-05",
    "CharterTypeID": 0,
    "FixtureStatusID": 0,
    "IsOwnersOption": False,
    "IsCOA": False,
}
rt_sf2 = {
    "FixtureID": 71338680,
    "MessageID": 20811043,
    "UpdatedDate": "2022-01-03T00:53:54",
    "ReceivedDate": "2022-01-03T00:52:35",
    "IMO": 9412995,
    "VesselClassID": 86,
    "OpenGeoID": 3153,
    "LoadGeoID": 3153,
    "OpenTaxonomyID": 2,
    "OpenDate": "2022-01-05",
    "CharterTypeID": 0,
    "FixtureStatusID": 0,
    "IsOwnersOption": False,
    "IsCOA": False,
}

# test new contact
rt_sf3 = {
    "FixtureID": 71338680,
    "MessageID": 20811043,
    "UpdatedDate": "2022-01-03T00:53:54",
    "ReceivedDate": "2022-01-03T00:52:35",
    "IMO": 9412995,
    "VesselClassID": 86,
    "OpenGeoID": 3153,
    "LoadGeoID": 3153,
    "OpenTaxonomyID": 2,
    "OpenDate": "2022-01-05",
    "CharterTypeID": 0,
    "FixtureStatusID": 0,
    "IsOwnersOption": False,
    "IsCOA": False,
    "ScrapedCargoType": "ums+ulsd",
    "ScrapedLoad2": "tes",
    "LoadGeoID2": 3153,
    "LoadName2": "testLoadName2",
    "LoadTaxonomyID2": 2,
    "LoadTaxonomy2": "testLoadTaxonomy2",
    "ScrapedDischarge2": "testDischarge",
    "DischargeGeoID2": 3153,
    "DischargeName2": "testDischargeName2",
    "DischargeTaxonomyID2": 2,
    "DischargeTaxonomy2": "testDischargeTaxonomy2",
    "Sender": "testSender",
}

rt_sf_3_model = ScrapedFixture(
    fixture_id=71338680,
    message_id=20811043,
    updated_date=datetime.fromisoformat("2022-01-03T00:53:54").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T00:52:35").replace(
        tzinfo=timezone.utc
    ),
    imo=9412995,
    vessel_class_id=86,
    open_geo_id=3153,
    load_geo_id=3153,
    open_taxonomy_id=2,
    open_date=datetime.fromisoformat("2022-01-05T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    charter_type_id=0,
    fixture_status_id=0,
    is_owners_option=False,
    is_coa=False,
    scraped_cargo_type="ums+ulsd",
    scraped_load2="tes",
    load_geo_id2=3153,
    load_name2="testLoadName2",
    load_taxonomy_id2=2,
    load_taxonomy2="testLoadTaxonomy2",
    scraped_discharge2="testDischarge",
    discharge_geo_id2=3153,
    discharge_name2="testDischargeName2",
    discharge_taxonomy_id2=2,
    discharge_taxonomy2="testDischargeTaxonomy2",
    sender="testSender",
)


rt_sf_1_model = ScrapedFixture(
    fixture_id=71338680,
    message_id=20811043,
    updated_date=datetime.fromisoformat("2022-01-03T00:53:54").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T00:52:35").replace(
        tzinfo=timezone.utc
    ),
    imo=9412995,
    vessel_class_id=86,
    open_geo_id=3153,
    load_geo_id=3778,
    open_taxonomy_id=2,
    open_date=datetime.fromisoformat("2022-01-05T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    charter_type_id=0,
    fixture_status_id=0,
    is_owners_option=False,
    is_coa=False,
)


sf_ras_tanura_2 = ScrapedFixture(
    fixture_id=71339469,
    message_id=20813261,
    updated_date=datetime.fromisoformat("2022-01-03T02:51:49").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T02:51:08").replace(
        tzinfo=timezone.utc
    ),
    imo=9383869,
    vessel_class_id=86,
    laycan_from=datetime.fromisoformat("2022-01-05T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    laycan_to=datetime.fromisoformat("2022-01-05T00:00:00").replace(
        tzinfo=timezone.utc
    ),
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
    charter_type_id=0,
    is_owners_option=False,
    is_coa=False,
)

sf_ras_tanura_1 = ScrapedFixture(
    fixture_id=71339456,
    message_id=20813261,
    updated_date=datetime.fromisoformat("2022-01-03T02:51:53").replace(
        tzinfo=timezone.utc
    ),
    received_date=datetime.fromisoformat("2022-01-03T02:51:08").replace(
        tzinfo=timezone.utc
    ),
    imo=9486934,
    vessel_class_id=86,
    laycan_from=datetime.fromisoformat("2022-01-01T00:00:00").replace(
        tzinfo=timezone.utc
    ),
    laycan_to=datetime.fromisoformat("2022-01-03T00:00:00").replace(
        tzinfo=timezone.utc
    ),
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
    charter_type_id=0,
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
    api = ScrapedFixturesAPI(connection, max_pages=2)
    return api, mocked_make_request


@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type",
    [
        (datetime(2022, 1, 1, 2, 0, 0), datetime(2022, 1, 4, 2, 59, 59), 1),
        # (datetime(2022,1,1), None, 1),
        # (None, None, 1),
        # (datetime(2022,1,1), datetime(2022,1,4), None)
    ],
)
def test_get_fixtures(received_date_from, received_date_to, vessel_type):

    mock_response = [
        sf1,
        sf2,
    ]
    api, connection = create_sf_api(mock_response)

    final_response = [sf_1_model, sf_2_model]

    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
    )

    assert results == final_response


@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type, port_id, vessel_class_id",
    [
        (
            datetime(2022, 1, 1, 2, 0, 0),
            datetime(2022, 1, 6, 2, 59, 59),
            1,
            3778,
            86,
        ),
        (
            datetime(2022, 1, 1, 2, 0, 0),
            datetime(2022, 1, 6, 2, 59, 59),
            1,
            3778,
            None,
        ),
    ],
)
def test_get_fixtures_by_port(
    received_date_from, received_date_to, vessel_type, port_id, vessel_class_id
):

    mock_response = [
        rt_sf1,
        rt_sf2,
    ]
    api, connection = create_sf_api(mock_response)
    # api = ScrapedFixturesAPI()

    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        port_id=port_id,
        vessel_class_id=vessel_class_id,
    )

    # exclude port that has not load geo in ras tanura(3778)
    final_response = [rt_sf_1_model]

    assert final_response == results


@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type, port_id",
    [
        (
            datetime(2022, 1, 1, 2, 0, 0),
            datetime(2022, 1, 6, 2, 59, 59),
            1,
            None,
        ),
    ],
)
def test_get_fixtures_by_port2(
    received_date_from, received_date_to, vessel_type, port_id
):

    mock_response = [
        sf1,
        sf2,
    ]
    api, connection = create_sf_api(mock_response)
    # api = ScrapedFixturesAPI()

    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        port_id=port_id,
    )

    # if user does not set the port is the function will return an empty object
    final_response = [sf_1_model, sf_2_model]

    assert final_response == results


# test new changes
@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type, port_id",
    [
        (
            datetime(2022, 1, 1, 2, 0, 0),
            datetime(2022, 1, 6, 2, 59, 59),
            1,
            None,
        ),
    ],
)
def test_get_fixtures_by_port3(
    received_date_from, received_date_to, vessel_type, port_id
):

    mock_response = [rt_sf3]
    api, connection = create_sf_api(mock_response)
    # api = ScrapedFixturesAPI()
    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        port_id=port_id,
    )

    # if user does not set the port is the function will return an empty object
    final_response = [rt_sf_3_model]

    assert final_response == results


# test deleted fixtures
@pytest.mark.parametrize(
    "received_date_from, received_date_to, vessel_type, port_id",
    [
        (
            datetime(2022, 1, 1, 2, 0, 0),
            datetime(2022, 1, 6, 20, 59, 59),
            1,
            None,
        ),
    ],
)
def test_get_fixtures_by_port3(
    received_date_from, received_date_to, vessel_type, port_id
):

    mock_response = [deleted_fixtures]
    mock_response += [rt_sf3]
    api, connection = create_sf_api(mock_response)
    # api = ScrapedFixturesAPI()

    results = api.get_fixtures(
        received_date_from=received_date_from,
        received_date_to=received_date_to,
        vessel_type=vessel_type,
        port_id=port_id,
    )

    # if user does not set the port is the function will return an empty object
    final_response = [rt_sf_3_model]

    assert final_response == results
