from dataclasses import dataclass
from typing import Tuple, Dict, Union
from unittest.mock import MagicMock

import requests

from signal_ocean import Connection
from signal_ocean.util.request_helpers import get_single, get_multiple

__test_response_1 = {'ModelID': 1, 'ModelName': 'model1'}
__test_response_2 = {'ModelID': 2, 'ModelName': 'model2'}
__test_responses = (__test_response_1, __test_response_2)


@dataclass(frozen=True)
class DummyModel:
    model_id: int
    model_name: str


__test_model_object_1 = DummyModel(model_id=1, model_name='model1')
__test_model_object_2 = DummyModel(model_id=2, model_name='model2')


def create_mock_connection(response_data:
                           Union[Dict, Tuple[Dict, ...], None]) \
        -> Tuple[Connection, MagicMock]:

    connection = Connection('', '')
    response = MagicMock()
    if response_data is None:
        response.status_code = requests.codes.not_found
    response.json.return_value = response_data
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    return connection, mocked_make_request


def test_get_single_returns_none_if_id_does_not_exist():
    relative_url = 'model/single/1'
    connection, _ = create_mock_connection(None)
    obj = get_single(connection, relative_url, DummyModel)
    assert obj is None


def test_get_single_requests_object_by_id():
    relative_url = 'model/single/1'
    connection, mocked_make_request = create_mock_connection(__test_response_1)
    _ = get_single(connection, relative_url, DummyModel)
    mocked_make_request.assert_called_with(relative_url)


def test_get_single_returns_object_by_id():
    relative_url = 'model/single/1'
    connection, _ = create_mock_connection(__test_response_1)
    obj = get_single(connection, relative_url, DummyModel)
    assert isinstance(obj, DummyModel)
    assert obj == __test_model_object_1


def test_get_multiple_requests():
    relative_url = 'model/all'
    connection, mocked_make_request = create_mock_connection(__test_responses)
    _ = get_multiple(connection, relative_url, DummyModel)
    mocked_make_request.assert_called_with(relative_url)


def test_get_single_returns():
    relative_url = 'model/single/1'
    connection, _ = create_mock_connection(__test_responses)
    objects = get_multiple(connection, relative_url, DummyModel)
    assert objects == (__test_model_object_1, __test_model_object_2)
