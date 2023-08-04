from typing import Tuple
from unittest.mock import MagicMock

import requests

from signal_ocean import Connection
from vessel_emissions_mock_data import __mock_emissions_response_imo_voyage_no_args, __mock_metrics_response, \
    __mock_emissions_response_imo_voyage_all_args, \
    __mock_emissions_imo_voyage_no_args, __mock_metrics_1, __mock_emissions_imo_voyage_all_args, \
    __mock_emissions_response_imo_no_args, __mock_emissions_imo_no_args, __mock_emissions_response_imo_one_arg, \
    __mock_emissions_imo_one_arg, __mock_emissions_response_imo_voyage_one_arg, __mock_emissions_imo_voyage_one_arg, \
    __mock_emissions_response_imo_all_args, __mock_emissions_imo_all_args
from vessel_class_emissions_mock_data import __mock_emissions_vessel_class_no_args, \
    __mock_emissions_response_vessel_class_no_args, \
    __mock_vessel_class_metrics_1, __mock_vessel_class_metrics_response_1, \
    __mock_emissions_response_vessel_class_one_arg, __mock_emissions_vessel_class_one_arg, \
    __mock_emissions_response_vessel_class_all_args, __mock_emissions_vessel_class_all_args
from mock_data_test import __mock_emissions_response_2, __mock_emissions_2
from signal_ocean.vessel_emissions.vessel_emissions_api import VesselEmissionsAPI


def create_vessel_emissions_api(response: requests.Response) -> Tuple[VesselEmissionsAPI, MagicMock]:
    connection = Connection()
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = VesselEmissionsAPI(connection)
    return api, mocked_make_request


def test_request_vessel_emissions_by_imo_and_voyage_number_no_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_voyage_no_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo_and_voyage_number(imo=9412036,
                                                           voyage_number=141)
    assert emissions == __mock_emissions_imo_voyage_no_args


def test_request_vessel_emissions_by_imo_and_voyage_number_one_arg():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_voyage_one_arg
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo_and_voyage_number(imo=9412036,
                                                           voyage_number=141,
                                                           include_efficiency_metrics=True)
    assert emissions == __mock_emissions_imo_voyage_one_arg


def test_request_vessel_emissions_by_imo_and_voyage_number_all_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_voyage_all_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo_and_voyage_number(imo=9412036,
                                                           voyage_number=141,
                                                           include_efficiency_metrics=True,
                                                           include_speed_statistics=True,
                                                           include_eu_emissions=True, include_consumptions=True,
                                                           include_durations=True,
                                                           include_distances=True)
    assert emissions == __mock_emissions_imo_voyage_all_args


def test_request_vessel_emissions_by_imo_no_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_no_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo(imo=9412036)
    assert emissions == __mock_emissions_imo_no_args


def test_request_vessel_emissions_by_imo_one_arg():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_one_arg
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo(imo=9412036)
    assert emissions == __mock_emissions_imo_one_arg


def test_request_vessel_emissions_by_imo_all_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_imo_all_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    emissions = api.get_emissions_by_imo(imo=9412036)
    assert emissions == __mock_emissions_imo_all_args


def test_request_vessel_metrics_by_imo():
    response = MagicMock()
    response.json.return_value = __mock_metrics_response
    api, mocked_make_request = create_vessel_emissions_api(response)
    metrics = api.get_metrics_by_imo(imo=9412036, year=2022)
    assert metrics == __mock_metrics_1


def test_request_vessel_class_emissions_no_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_vessel_class_no_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    metrics = api.get_emissions_by_vessel_class_id(vessel_class_id=86)
    assert metrics == __mock_emissions_vessel_class_no_args


def test_request_vessel_class_emissions_one_arg():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_vessel_class_one_arg
    api, mocked_make_request = create_vessel_emissions_api(response)
    metrics = api.get_emissions_by_vessel_class_id(vessel_class_id=86)
    assert metrics == __mock_emissions_vessel_class_one_arg


def test_request_vessel_class_emissions_all_args():
    response = MagicMock()
    response.json.return_value = __mock_emissions_response_vessel_class_all_args
    api, mocked_make_request = create_vessel_emissions_api(response)
    metrics = api.get_emissions_by_vessel_class_id(vessel_class_id=86)
    assert metrics == __mock_emissions_vessel_class_all_args


def test_request_vessel_class_metrics():
    response = MagicMock()
    response.json.return_value = __mock_vessel_class_metrics_response_1
    api, mocked_make_request = create_vessel_emissions_api(response)
    metrics = api.get_metrics_by_vessel_class_id(vessel_class_id=86)
    assert metrics == __mock_vessel_class_metrics_1
