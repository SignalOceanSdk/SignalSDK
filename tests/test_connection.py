from signal_ocean import Connection
from unittest.mock import patch


def test_uses_api_key_from_environment_variables_by_default():
    key_from_env_var = 'key from env var'
    with patch.dict('os.environ', {'SIGNAL_OCEAN_API_KEY': key_from_env_var}, clear=True):
        connection = Connection()

        assert connection._headers['Api-Key'] == key_from_env_var


def test_uses_provided_api_key():
    provided_key = 'provided key'
    connection = Connection(api_key=provided_key)

    assert connection._headers['Api-Key'] == provided_key


def test_has_no_api_key_if_not_provided_and_no_environment_variable():
    with patch.dict('os.environ', {}, clear=True):
        connection = Connection()

        assert connection._headers['Api-Key'] is None


def test_targets_production_host_by_default():
    with patch.dict('os.environ', {}, clear=True):
        connection = Connection()

        assert connection._api_host == 'https://signalprodapims.azure-api.net/'


def test_host_can_be_overridden_via_parameter():
    overridden_host = 'overridden host'
    connection = Connection(api_host=overridden_host)

    assert connection._api_host == overridden_host


def test_host_can_be_overridden_via_environment_variable():
    overridden_host = 'overridden host'
    with patch.dict('os.environ', {'SIGNAL_OCEAN_API_HOST': overridden_host}, clear=True):
        connection = Connection()

        assert connection._api_host == overridden_host
