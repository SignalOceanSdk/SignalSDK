import json
from datetime import date
from typing import Union
from unittest.mock import MagicMock

import pytest
import requests

from signal_ocean.supply import (
    EtaConfigurationWithRestrictions,
    LiveSupplyFilter,
    SupplyAPI,
    SupplyFilter,
    SupplySnapshot,
    SupplyTrend,
)
from signal_ocean.supply.templates import build_filter_body, find_template

TREND = "supply-api/v1/supply/supply-trend"
HISTORICAL = "supply-api/v1/supply/historical-raw-data"
LIVE = "supply-api/v1/supply/supply"


def make_response(status: int, body: Union[dict, str]) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response.reason = {200: "OK", 400: "Bad Request", 403: "Forbidden",
                       429: "Too Many Requests", 502: "Bad Gateway"}[status]
    response.url = "https://gateway.test/" + TREND
    response.encoding = "utf-8"
    text = body if isinstance(body, str) else json.dumps(body)
    response._content = text.encode("utf-8")
    return response


def create_api(response: requests.Response):
    connection = MagicMock()
    connection._make_post_request.return_value = response
    return SupplyAPI(connection), connection


def test_trend_posts_dates_and_template_body():
    api, connection = create_api(make_response(200, {
        "supplyPerDay": [{"date": "2026-10-01T00:00:00Z", "supply": 12}],
        "notes": ["note"],
    }))

    trend = api.get_supply_trend(
        date(2026, 10, 1), date(2026, 10, 31), template="TD3C"
    )

    connection._make_post_request.assert_called_once_with(
        TREND,
        {
            "startDate": "2026-10-01",
            "endDate": "2026-10-31",
            **build_filter_body(find_template("TD3C"), None),
        },
        headers=None,
    )
    assert isinstance(trend, SupplyTrend)
    assert trend.supply_per_day[0].supply == 12
    assert trend.notes == ("note",)


def test_historical_sends_one_day():
    api, connection = create_api(make_response(200, {"data": []}))

    snapshot = api.get_historical_supply(
        date(2026, 10, 15), filters=SupplyFilter(vessel_class="Aframax")
    )

    connection._make_post_request.assert_called_once_with(
        HISTORICAL,
        {
            "startDate": "2026-10-15",
            "endDate": "2026-10-15",
            "vesselClass": "Aframax",
        },
        headers=None,
    )
    assert isinstance(snapshot, SupplySnapshot)


@pytest.mark.parametrize(
    "use_only_hub_ports, headers",
    [
        (True, {"UseOnlyHubPorts": "true"}),
        (False, {"UseOnlyHubPorts": "false"}),
        (None, None),
    ],
)
def test_historical_hub_ports_header(use_only_hub_ports, headers):
    api, connection = create_api(make_response(200, {"data": []}))

    api.get_historical_supply(
        date(2026, 10, 15),
        filters=SupplyFilter(vessel_class="Aframax"),
        use_only_hub_ports=use_only_hub_ports,
    )

    assert connection._make_post_request.call_args.kwargs == {
        "headers": headers
    }


def test_live_has_no_dates_and_include_details_only_when_true():
    api, connection = create_api(make_response(200, {"data": []}))
    filters = SupplyFilter(vessel_class="Aframax")

    default = api.get_live_supply(filters=filters)
    connection._make_post_request.assert_called_with(
        LIVE, {"vesselClass": "Aframax"}, headers=None
    )
    detailed = api.get_live_supply(filters=filters, include_details=True)
    connection._make_post_request.assert_called_with(
        LIVE, {"vesselClass": "Aframax", "includeDetails": True}, headers=None
    )

    assert default.include_details is False
    assert detailed.include_details is True


def test_live_sends_restrictions():
    api, connection = create_api(make_response(200, {"data": []}))

    api.get_live_supply(filters=LiveSupplyFilter(
        vessel_class="Aframax",
        eta_configuration=[EtaConfigurationWithRestrictions(
            basis_port_id=3853, restrictions="Suez"
        )],
    ))

    body = connection._make_post_request.call_args.args[1]
    assert body["etaConfiguration"][0]["restrictions"] == "Suez"


def _error_message(response: requests.Response) -> str:
    api, _ = create_api(response)
    with pytest.raises(requests.HTTPError) as error:
        api.get_supply_trend(date(2026, 10, 1), date(2026, 10, 2))
    assert error.value.response is response
    return str(error.value)


def test_error_includes_validation_message():
    message = _error_message(make_response(400, {
        "title": "One or more validation errors occurred.",
        "status": 400,
        "errors": {"startDate": [
            "The date range between StartDate and EndDate must not exceed "
            "1 day."
        ]},
    }))

    assert "400" in message
    assert (
        "The date range between StartDate and EndDate must not exceed 1 day."
        in message
    )


def test_error_includes_tracking_id():
    title = (
        "You currently do not have access to the following vessel classes: "
        "VLCC, Suezmax."
    )

    message = _error_message(make_response(403, {
        "title": title, "status": 403, "TrackingId": "trk-0001",
    }))

    assert title in message
    assert "trk-0001" in message


def test_error_includes_quota_message():
    message = _error_message(make_response(403, {
        "statusCode": 403,
        "message": "Out of call volume quota. Quota will be replenished in "
                   "09:52:20.",
    }))

    assert "Out of call volume quota" in message


def test_error_with_html_body():
    message = _error_message(
        make_response(502, "<html><body>Upstream timed out</body></html>")
    )

    assert "502" in message
    assert "Upstream timed out" in message


def test_error_with_unknown_json_body_shows_body_text():
    message = _error_message(make_response(400, {
        "error": {"code": "InvalidInput", "detail": "Unknown vessel class"}
    }))

    assert "Unknown vessel class" in message


def test_public_exports():
    from signal_ocean.supply import (  # noqa: F401
        SupplyTemplate,
        VesselClass,
    )
