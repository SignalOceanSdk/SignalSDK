import json
from datetime import date
from unittest.mock import MagicMock

import pytest

pytest.importorskip("mcp")

import anyio  # noqa: E402

from signal_ocean.supply import (  # noqa: E402
    SupplyAPI,
    SupplyFilter,
    SupplyRecord,
    SupplySnapshot,
    SupplyTrend,
)
from signal_ocean_mcp import server  # noqa: E402


@pytest.fixture
def api(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(server, "_supply_api", mock, raising=False)
    return mock


def test_trend_tool_parses_dates_and_template(api):
    api.get_supply_trend.return_value = SupplyTrend()

    result = anyio.run(
        server.get_supply_trend, "2026-10-01", "2026-10-02", "TD3C", None
    )

    api.get_supply_trend.assert_called_once_with(
        date(2026, 10, 1), date(2026, 10, 2), template="TD3C", filters=None
    )
    assert json.loads(result) == {"supplyPerDay": [], "notes": []}


def test_filters_accept_api_names(api):
    api.get_supply_trend.return_value = SupplyTrend()

    anyio.run(
        server.get_supply_trend, "2026-10-01", "2026-10-02", None,
        {"vesselClass": "Aframax"},
    )

    filters = api.get_supply_trend.call_args.kwargs["filters"]
    assert isinstance(filters, SupplyFilter)
    assert filters.vessel_class == "Aframax"


def test_snapshot_tool_truncates(api):
    api.get_live_supply.return_value = SupplySnapshot(data=(
        SupplyRecord(imo=1), SupplyRecord(imo=2), SupplyRecord(imo=3),
    ))

    result = json.loads(anyio.run(server.get_live_supply, None, None, 2))

    assert result["count"] == 3
    assert result["truncated"] is True
    assert [record["imo"] for record in result["data"]] == [1, 2]


def test_templates_tool_lists_codes(monkeypatch):
    monkeypatch.setattr(
        server, "_supply_api", SupplyAPI(MagicMock()), raising=False
    )
    server._supply_templates_sync.cache_clear()

    result = json.loads(anyio.run(server.get_supply_templates))

    assert len(result) == 28
    assert result[0] == {
        "code": "TD1",
        "name": "VLCC US Gulf Supply 30 Days (TD1)",
        "description": "US Gulf crude supply to Loop, available next 30 days",
        "segment": "Tanker",
    }
