from decimal import Decimal
from unittest.mock import patch, MagicMock, ANY
from typing import Tuple
from datetime import datetime

import requests
from signal_ocean import Connection


from signal_ocean.scraped_fixtures import ScrapedFixturesAPI

example_request_1 ={
                    "ReceivedDateFrom": datetime(2022,1,1),
                    "ReceivedDateTo": datetime(2022,1,4),
                    "VesselType": 1
                   }

def create_valuations_api(
    response: requests.Response) -> Tuple[ScrapedFixturesAPI, Connection]:
    connection = MagicMock()
    connection._make_get_request.return_value = response
    api = ScrapedFixturesAPI(connection)

    return (api, connection)


def test_get_fixtures():

    response = MagicMock()
    response.text = None
    api, connection = create_valuations_api(response)

    results = api.get_fixtures(
        received_date_from=example_request_1['ReceivedDateFrom'],
        received_date_to=example_request_1['ReceivedDateTo'],
        vessel_type=example_request_1['VesselType'],
        )

    while True:
        try:
            print(next(results))
        except StopIteration:
            break

test_get_fixtures()




