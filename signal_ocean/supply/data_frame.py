"""Conversion of Supply API results to pandas data frames."""
from typing import TYPE_CHECKING, Any, Dict, List

import pandas as pd
from pydantic import BaseModel

from .._internals import IterableConstants

if TYPE_CHECKING:
    from .models import SupplySnapshot, SupplyTrend


class Column(metaclass=IterableConstants):
    """Column names of `SupplySnapshot.to_data_frame()`.

    After these columns come four columns per ETA configuration:
    `eta_<id>`, `eta_distance_<id>`, `eta_basis_port_id_<id>` and
    `eta_canals_<id>`. `<id>` is the configuration's `id`, or its position
    (`0`, `1`, ...) when it has no `id`.
    """

    DAY = "day"
    """The snapshot day."""

    IMO = "imo"
    """The vessel's IMO number."""

    VESSEL_CLASS_ID = "vessel_class_id"
    """The vessel class."""

    VESSEL_CLASS = "vessel_class"
    """The vessel class name."""

    OPEN_LOCATION = "open_location"
    """Name of the location where the vessel opens."""

    OPEN_LOCATION_TAXONOMY = "open_location_taxonomy"
    """Level of the open location, for example `Port`."""

    OPEN_LOCATION_GEO_ID = "open_location_geo_id"
    """Geo id of the open location."""

    OPEN_LOCATION_TAXONOMY_ID = "open_location_taxonomy_id"
    """Level id of the open location."""

    OPEN_DATE_FROM = "open_date_from"
    """Start of the open period."""

    OPEN_DATE_TO = "open_date_to"
    """End of the open period."""

    AVAILABILITY_STATE = "availability_state"
    """Commercial availability state, for example `Available`."""

    AVAILABILITY_STATE_ID = "availability_state_id"
    """Id of the availability state."""

    MARKET_STATUS = "market_status"
    """Market push state, for example `Pushed`."""

    MARKET_STATUS_ID = "market_status_id"
    """Id of the market status."""

    MARKET_DEPLOYMENT = "market_deployment"
    """Market deployment, for example `Spot`."""

    MARKET_DEPLOYMENT_ID = "market_deployment_id"
    """Id of the market deployment."""

    POSITION_SOURCE_ORIGIN = "position_source_origin"
    """Origin of the position data, for example `Manual`."""

    POSITION_SOURCE_ORIGIN_ID = "position_source_origin_id"
    """Id of the position source origin."""

    POSITION_SOURCE_TYPE = "position_source_type"
    """Type of the position source, for example `Email`."""

    POSITION_SOURCE_TYPE_ID = "position_source_type_id"
    """Id of the position source type."""

    LAST_MARKETED_DATE = "last_marketed_date"
    """Last date the vessel was pushed to the market."""

    LATEST_UPDATED_DATE = "latest_updated_date"
    """Last update of the vessel's commercial data."""

    FORECASTED_DESTINATION_PORT = "forecasted_destination_port"
    """Name of the forecasted next port."""

    FORECASTED_DESTINATION_PORT_ID = "forecasted_destination_port_id"
    """Id of the forecasted next port."""

    VOYAGE_STATE = "voyage_state"
    """Operational voyage state, for example `Laden`."""

    VOYAGE_STATE_ID = "voyage_state_id"
    """Id of the voyage state."""

    CARGO_TYPE = "cargo_type"
    """Name of the current or last cargo type."""

    CARGO_TYPE_ID = "cargo_type_id"
    """Id of the current or last cargo type."""

    CARGO_QUANTITY = "cargo_quantity"
    """Cargo quantity in metric tons."""

    CHARTERER = "charterer"
    """Charterer name."""

    CHARTERER_ID = "charterer_id"
    """Charterer company id."""

    START_PORT = "start_port"
    """Name of the voyage leg's start port."""

    START_PORT_ID = "start_port_id"
    """Id of the voyage leg's start port."""

    LAST_VOYAGE_CARGO_TYPES = "last_voyage_cargo_types"
    """Cargo type names of the previous voyage, as a list."""

    LAST_VOYAGE_CARGO_TYPE_IDS = "last_voyage_cargo_type_ids"
    """Cargo type ids of the previous voyage, as a list."""

    LAST_CARGO_TYPES = "last_cargo_types"
    """Last cargo type names, as a list."""

    LAST_CARGO_TYPE_IDS = "last_cargo_type_ids"
    """Last cargo type ids, as a list."""

    LAST_MOVEMENT_DATE_TIME_UTC = "last_movement_date_time_utc"
    """Last time the vessel moved."""

    DAYS_SINCE_LATEST_AIS = "days_since_latest_ais"
    """Days since the last AIS message."""

    AIS_LATITUDE_AVERAGE = "ais_latitude_average"
    """Average latitude of the day."""

    AIS_LONGITUDE_AVERAGE = "ais_longitude_average"
    """Average longitude of the day."""

    AIS_DRAUGHT_AVERAGE = "ais_draught_average"
    """Average draught of the day."""

    AIS_HEADING_AVERAGE = "ais_heading_average"
    """Average heading of the day."""

    AIS_SPEED_AVERAGE = "ais_speed_average"
    """Average speed of the day, stationary time included."""

    AIS_SEAGOING_SPEED_AVERAGE = "ais_seagoing_speed_average"
    """Average speed of the day when steaming (5 knots or more)."""

    AIS_CURRENT_AREA = "ais_current_area"
    """Name of the area the vessel is in."""

    AIS_CURRENT_AREA_ID = "ais_current_area_id"
    """Id of the area the vessel is in."""

    AIS_CLOSEST_LOCATION = "ais_closest_location"
    """Name of the closest location."""

    AIS_CLOSEST_LOCATION_ID = "ais_closest_location_id"
    """Id of the closest location."""

    AIS_DESTINATION = "ais_destination"
    """Name of the destination the crew reported in AIS."""

    AIS_DESTINATION_TAXONOMY = "ais_destination_taxonomy"
    """Level of the AIS destination, for example `Port`."""

    AIS_DESTINATION_GEO_ID = "ais_destination_geo_id"
    """Geo id of the AIS destination."""

    AIS_DESTINATION_TAXONOMY_ID = "ais_destination_taxonomy_id"
    """Level id of the AIS destination."""

    ETA_TO_AIS_DESTINATION = "eta_to_ais_destination"
    """Calculated ETA to the AIS destination."""

    MILES_TO_AIS_DESTINATION = "miles_to_ais_destination"
    """Distance to the AIS destination in nautical miles."""

    DELAYS_TO_AIS_DESTINATION = "delays_to_ais_destination"
    """Estimated delay to the AIS destination in hours."""

    NOTES = "notes"
    """Your company's notes; only when live supply includes details."""


def snapshot_to_data_frame(snapshot: "SupplySnapshot") -> pd.DataFrame:
    """Flatten vessel records into one row per vessel."""
    columns = [column for column in Column if column != Column.NOTES]
    if snapshot.include_details:
        columns.append(Column.NOTES)
    eta_columns: List[str] = []
    rows = []

    for record in snapshot.data:
        row: Dict[str, Any] = {
            Column.DAY: record.day,
            Column.IMO: record.imo,
            Column.VESSEL_CLASS_ID: record.vessel_class_id,
            Column.VESSEL_CLASS: record.vessel_class,
        }
        for category in (
            record.commercial_availability,
            record.voyage_details,
            record.ais_tracking,
        ):
            if category is not None:
                row.update(_values(category))
        if snapshot.include_details:
            details = record.details
            row[Column.NOTES] = details.notes if details else None
        for position, eta in enumerate(record.eta_details):
            key = eta.id or str(position)
            values = {
                f"eta_{key}": eta.eta,
                f"eta_distance_{key}": eta.distance,
                f"eta_basis_port_id_{key}": eta.basis_port_id,
                f"eta_canals_{key}": _cell(eta.canals),
            }
            eta_columns += [n for n in values if n not in eta_columns]
            row.update(values)
        rows.append(row)

    return pd.DataFrame(rows, columns=columns + eta_columns)


def trend_to_data_frame(trend: "SupplyTrend") -> pd.DataFrame:
    """Return the daily counts indexed by date."""
    index = pd.DatetimeIndex(
        [day.date for day in trend.supply_per_day], name="date"
    )
    supply = [day.supply for day in trend.supply_per_day]
    return pd.DataFrame({"supply": supply}, index=index)


def _values(category: BaseModel) -> Dict[str, Any]:
    return {
        name: _cell(getattr(category, name))
        for name in type(category).model_fields
    }


def _cell(value: Any) -> Any:
    return list(value) if isinstance(value, tuple) else value
