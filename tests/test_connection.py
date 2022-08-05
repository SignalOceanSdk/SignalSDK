from unittest.mock import patch

import pytest

from signal_ocean import Connection


def test_uses_api_key_from_environment_variables_by_default():
    key_from_env_var = "key from env var"
    connection = Connection()

    with patch.dict(
        "os.environ", {"SIGNAL_OCEAN_API_KEY": key_from_env_var}, clear=True
    ), patch("requests.get") as get:
        connection._make_get_request(None)

    assert get.call_args.kwargs["headers"]["Api-Key"] == key_from_env_var


def test_uses_provided_api_key():
    provided_key = "provided key"
    connection = Connection(api_key=provided_key)

    with patch.dict("os.environ", clear=True), patch("requests.get") as get:
        connection._make_get_request(None)

    assert get.call_args.kwargs["headers"]["Api-Key"] == provided_key


def test_has_no_api_key_if_not_provided_and_no_environment_variable():
    connection = Connection()

    with patch.dict("os.environ", {}, clear=True), patch(
        "requests.get"
    ) as get:
        connection._make_get_request(None)

    assert get.call_args.kwargs["headers"]["Api-Key"] is None


def test_targets_production_host_by_default():
    connection = Connection()

    with patch.dict("os.environ", {}, clear=True), patch(
        "requests.get"
    ) as get:
        connection._make_get_request(None)

    assert get.call_args.args == ("https://api-gateway.signalocean.com/",)


@pytest.mark.parametrize("overridden_host", ["host", "host/"])
def test_host_can_be_overridden_via_parameter(overridden_host: str):
    connection = Connection(api_host=overridden_host)

    with patch.dict("os.environ", {}, clear=True), patch(
        "requests.get"
    ) as get:
        connection._make_get_request(None)

    assert get.call_args.args == ("host/",)


@pytest.mark.parametrize("overridden_host", ["host", "host/"])
def test_host_can_be_overridden_via_environment_variable(overridden_host: str):
    connection = Connection()

    with patch.dict(
        "os.environ", {"SIGNAL_OCEAN_API_HOST": overridden_host}, clear=True
    ), patch("requests.get") as get:
        connection._make_get_request(None)

    assert get.call_args.args == ("host/",)


def test_makes_get_requests_with_specified_parameters():
    connection = Connection("api_key", "api_host")
    query_string = {"key": "value"}

    with patch("requests.get") as get:
        connection._make_get_request("relative_url", query_string)

    get.assert_called_with(
        "api_host/relative_url",
        params=query_string,
        headers={
            "Api-Key": "api_key",
            "Content-Type": "application/json",
            "Source": "SignalSDK",
        },
    )
