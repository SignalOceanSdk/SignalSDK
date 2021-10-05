import dataclasses
from copy import copy
from datetime import datetime, date, timezone
from typing import Tuple, Dict, Union, List
from unittest.mock import MagicMock
from urllib.parse import urljoin

import pytest

from signal_ocean import Connection
from signal_ocean.oilx_cargo_tracking.oilx_models import CargoFlow, \
    CargoFlowsPagedResponse
from signal_ocean.oilx_cargo_tracking.oilx_cargo_tracking_api import OilxCargoTrackingAPI

_mock_oilx_cargo_data_1 = {
        "ID": "O7408081L8D1DFC642039400U8D1F60A03CFB380",
        "IMO": 7408081,
        "VesselClassID": 86,
        "VesselName": "Leo",
        "LoadDate": "2014-12-06T23:48:24Z",
        "LoadGeoAssetID": 6372,
        "DischargeDate": "2015-01-04T07:48:51Z",
        "DischargeGeoAssetID": 4698,
        "LoadPortID": 3281,
        "LoadStsIndicator": 0,
        "CrudeOilGradeID": 5053,
        "CrudeOilGradeName": "Chile Crude Oil",
        "CrudeOilGradeGroupID": 130000,
        "CrudeOilGradeGroupName": "Dirty",
        "APIGravity": 37.30,
        "GravityBand": "Light",
        "SulphurContent": 0.0500,
        "SulphurBand": "Sweet",
        "OriginCountryID": 53,
        "OriginCountryName": "Chile",
        "LoadQuantityKiloTonnes": 24.928,
        "LoadQuantityKiloBarrels": 187.033,
        "DischargePortID": 3845,
        "DischargeStsIndicator": 0,
        "SupplierName": "Not set",
        "BuyerName": "Not set",
        "LoadCountryGroupID": 4,
        "LoadCountryGroupName": "OECD Americas",
        "DischargeCountryGroupID": 4,
        "DischargeCountryGroupName": "OECD Americas",
        "DischargeSubCountryID": 3,
        "DischargeSubCountryName": "PADD 3: Gulf Coast",
        "DestinationCountryID": 240,
        "DestinationCountryName": "United States",
        "VoyageID": "I7109D1VECBC28100",
        "LoadEventID": "I7109D1TECC119B00",
        "DischargeEventID": "I7109D1TECC2BF900",
        "LoadEventDetailID": "I7109D1LECC119B00",
        "DischargeEventDetailID": "I7109D1LECC2BF900",
        "Deleted": false
    }

_mock_oilx_cargo_data_2 = {
        "ID": "O7408081L8D1DFC642039400U8D1FBE703758080",
        "IMO": 7408081,
        "VesselClassID": 86,
        "VesselName": "Leo",
        "LoadDate": "2014-12-06T23:48:24Z",
        "LoadGeoAssetID": 6372,
        "DischargeDate": "2015-01-11T18:53:25Z",
        "DischargeGeoAssetID": 5436,
        "LoadPortID": 3281,
        "LoadStsIndicator": 0,
        "CrudeOilGradeID": 5053,
        "CrudeOilGradeName": "Chile Crude Oil",
        "CrudeOilGradeGroupID": 130000,
        "CrudeOilGradeGroupName": "Dirty",
        "APIGravity": 37.30,
        "GravityBand": "Light",
        "SulphurContent": 0.0500,
        "SulphurBand": "Sweet",
        "OriginCountryID": 53,
        "OriginCountryName": "Chile",
        "LoadQuantityKiloTonnes": 24.928,
        "LoadQuantityKiloBarrels": 187.033,
        "DischargePortID": 3845,
        "DischargeStsIndicator": 0,
        "SupplierName": "Not set",
        "BuyerName": "Not set",
        "LoadCountryGroupID": 4,
        "LoadCountryGroupName": "OECD Americas",
        "DischargeCountryGroupID": 4,
        "DischargeCountryGroupName": "OECD Americas",
        "DischargeSubCountryID": 3,
        "DischargeSubCountryName": "PADD 3: Gulf Coast",
        "DestinationCountryID": 240,
        "DestinationCountryName": "United States",
        "VoyageID": "I7109D1VECBC28100",
        "LoadEventID": "I7109D1TECC119B00",
        "DischargeEventID": "I7109D1TECC2BF900",
        "LoadEventDetailID": "I7109D1LECC119B00",
        "DischargeEventDetailID": "I7109D1LECC392800",
        "Deleted": false
    }


_mock_oilx_cargoes_paged_response_data_1 = {
    'NextPageToken': 'ASDF',
    'Data': [_mock_oilx_cargo_data_1]
}

_mock_oilx_cargoes_paged_response_data_2 = {
    'NextPageToken': 'ABCD',
    'Data': [_mock_oilx_cargo_data_2]
}

_mock_oilx_cargo_1 = CargoFlow(_mock_oilx_cargo_data_1)

_mock_oilx_cargo_2 = CargoFlow(_mock_oilx_cargo_data_2)

_mock_oilx_cargoes = [_mock_oilx_cargo_1, _mock_oilx_cargo_2]


@pytest.mark.parametrize("vessel_class_id, incremental",
                         [(None, False,
                           'oilx-cargo-tracking-api/v1/cargoTracking'),
                          (None, True,
                           'oilx-cargo-tracking-api/v1/cargoTracking/incremental'),
                          (84, False,
                           'oilx-cargo-tracking-api/v1/cargoTracking/class/84'),
                          ( 84, True,
                           'oilx-cargo-tracking-api/v1/cargoTracking/84/incremental')])
def test_get_endpoint(vessel_class_id, incremental, expected):
    endpoint = OilxCargoTrackingAPI._get_endpoint(
        vessel_class_id=vessel_class_id,
        incremental=incremental)
    assert endpoint == expected


def test_get_endpoint_error_no_arguments():
    with pytest.raises(NotImplementedError):
        OilxCargoTrackingAPI._get_endpoint()


def test_get_endpoint_error_vessel_type_non_incremental():
    with pytest.raises(NotImplementedError):
        OilxCargoTrackingAPI._get_endpoint(vessel_type_id=1,
                                 incremental=False)


def create_oilx_cargo_tracking_api(response_data: Union[Dict, List] = None) \
        -> Tuple[OilxCargoTrackingAPI, MagicMock]:
    connection = Connection('', '')
    response = MagicMock()
    response.json.return_value = response_data
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = OilxCargoTrackingAPI(connection)
    return api, mocked_make_request


def test_oilx_cargo_tracking_api_pages():
    mock_response = _mock_oilx_cargoes_paged_response_data_1
    api, _ = create_oilx_cargo_tracking_api(mock_response)
    oilx_cargoes, _ = api._get_oilx_cargoes_pages('')
    assert oilx_cargoes == _mock_oilx_cargoes


def test_get_oilx_cargoes_vessel_class_requests():
    mock_response = _mock_oilx_cargoes_paged_response_data_1
    next_page_token = \
        _mock_oilx_cargoes_paged_response_data_1['NextPageToken']
    vessel_class_id = 86
    api, mocked_make_request = create_oilx_cargo_tracking_api(
        mock_response)
    _ = api.get_oilx_cargoes(vessel_class_id=vessel_class_id)
    mocked_make_request.assert_called_with(
        urljoin(OilxCargoTrackingAPI.relative_url, f'cargoTracking/class/{vessel_class_id}'),
        query_string={'token': next_page_token})


def test_get_oilx_cargoes_class_returns():
    mock_response = _mock_oilx_cargoes_paged_response_data_1
    api, _ = create_oilx_cargo_tracking_api(mock_response)
    oilx_cargoes = api.get_oilx_cargoes(vessel_class_id=86)
    assert oilx_cargoes == mock_response

