import json
from datetime import datetime, timezone
from pathlib import Path

from signal_ocean.supply import (
    AisTracking,
    Column,
    CommercialAvailability,
    DailySupply,
    SupplyEta,
    SupplyRecord,
    SupplySnapshot,
    SupplyTrend,
    VesselDetails,
    VoyageDetails,
)

SAMPLE = Path(__file__).parent / "sample_supply_response.json"
STATIC = [column for column in Column if column != Column.NOTES]
ETA_TIME = datetime(2026, 10, 2, tzinfo=timezone.utc)


def _sample_snapshot(**kwargs):
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))["data"]
    return SupplySnapshot(
        data=tuple(SupplyRecord.model_validate(r) for r in data), **kwargs
    )


def _eta(eta_id, distance):
    return SupplyEta(
        id=eta_id, basis_port_id=3853, eta=ETA_TIME, distance=distance,
        canals=("Suez",),
    )


def test_snapshot_columns_follow_models():
    assert STATIC == (
        ["day", "imo", "vessel_class_id", "vessel_class"]
        + list(CommercialAvailability.model_fields)
        + list(VoyageDetails.model_fields)
        + list(AisTracking.model_fields)
    )
    assert list(_sample_snapshot().to_data_frame().columns) == STATIC


def test_notes_column_only_with_include_details():
    record = SupplyRecord(imo=1, details=VesselDetails(notes="note"))

    with_details = SupplySnapshot(data=(record,), include_details=True)
    without = SupplySnapshot(data=(record,))

    frame = with_details.to_data_frame()
    assert list(frame.columns) == STATIC + ["notes"]
    assert frame["notes"].tolist() == ["note"]
    assert "notes" not in without.to_data_frame().columns


def test_eta_columns_per_config_id():
    snapshot = SupplySnapshot(data=(
        SupplyRecord(imo=1, eta_details=(_eta("A", 10.0), _eta("B", 20.0))),
        SupplyRecord(imo=2, eta_details=(_eta("A", 30.0), _eta("B", 40.0))),
    ))

    frame = snapshot.to_data_frame()

    assert list(frame.columns)[len(STATIC):] == [
        "eta_A", "eta_distance_A", "eta_basis_port_id_A", "eta_canals_A",
        "eta_B", "eta_distance_B", "eta_basis_port_id_B", "eta_canals_B",
    ]
    assert frame["eta_distance_A"].tolist() == [10.0, 30.0]
    assert frame["eta_distance_B"].tolist() == [20.0, 40.0]
    assert frame["eta_canals_B"].tolist() == [["Suez"], ["Suez"]]


def test_eta_without_id_uses_position():
    snapshot = SupplySnapshot(data=(
        SupplyRecord(imo=1, eta_details=(_eta(None, 1.0), _eta(None, 2.0))),
    ))

    frame = snapshot.to_data_frame()

    assert frame["eta_distance_0"].tolist() == [1.0]
    assert frame["eta_distance_1"].tolist() == [2.0]


def test_empty_snapshot_has_static_columns():
    frame = SupplySnapshot().to_data_frame()

    assert len(frame) == 0
    assert list(frame.columns) == STATIC


def test_trend_frame():
    trend = SupplyTrend(supply_per_day=(
        DailySupply(date=datetime(2026, 10, 1, tzinfo=timezone.utc),
                    supply=12),
        DailySupply(date=datetime(2026, 10, 2, tzinfo=timezone.utc),
                    supply=15),
    ))

    frame = trend.to_data_frame()
    empty = SupplyTrend().to_data_frame()

    assert frame.index.name == "date"
    assert frame["supply"].tolist() == [12, 15]
    assert len(empty) == 0
    assert empty.index.name == "date"
    assert list(empty.columns) == ["supply"]
