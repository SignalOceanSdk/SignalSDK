"""Response models of the Supply API.

Attribute names are the API response names in snake_case.
"""
from datetime import datetime
from typing import Any, Optional, Tuple, Union

import pandas as pd
from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from ._base import SupplyResponseModel
from .data_frame import snapshot_to_data_frame, trend_to_data_frame


def _none_to_empty(value: Any) -> Any:
    return () if value is None else value


_EMPTY_IF_NULL = BeforeValidator(_none_to_empty)


class DailySupply(SupplyResponseModel):
    """The supply count of one day.

    Attributes:
        date: The snapshot day.
        supply: Number of vessels that match the filters on that day.
    """

    date: datetime
    supply: int


class SupplyTrend(SupplyResponseModel):
    """The result of a supply trend request.

    Attributes:
        supply_per_day: One count per day of the requested range.
        notes: Messages from the API, for example about ETA basis ports
            that were remapped to hub ports.
    """

    supply_per_day: Annotated[
        Tuple[DailySupply, ...], _EMPTY_IF_NULL
    ] = ()
    notes: Annotated[Tuple[str, ...], _EMPTY_IF_NULL] = ()

    def to_data_frame(self) -> pd.DataFrame:
        """Return the counts as a data frame.

        Returns:
            A data frame indexed by `date`, oldest day first, with one
            column `supply`.
        """
        return trend_to_data_frame(self)


class CommercialAvailability(SupplyResponseModel):
    """Open location, open dates and commercial status of a vessel.

    Attributes:
        open_location: Name of the location where the vessel becomes
            available.
        open_location_taxonomy: Precision level of the open location, for
            example `Port`.
        open_location_geo_id: Geo id of the open location.
        open_location_taxonomy_id: Precision level id of the open location.
            See `LocationTaxonomy`.
        open_date_from: Start of the open period: the first day of the lay
            range.
        open_date_to: End of the open period: the last day of the lay range.
        availability_state: Charter market status: open for new business,
            under negotiation, or committed. Shows if the vessel is in the
            live tonnage pool. See `AvailabilityState`.
        availability_state_id: Id of the availability state.
        market_status: Whether the commercial operator markets the vessel:
            pushed (listed), possibly pushed, or not pushed (no evidence).
            See `MarketStatus`.
        market_status_id: Id of the market status.
        market_deployment: How the vessel is deployed: spot (voyage by
            voyage), program (semi-contractual), contract (long term) or
            relet (sub-chartered). See `MarketDeployment`.
        market_deployment_id: Id of the market deployment.
        position_source_origin: How the position was found: entered by a
            user, from AIS, or calculated by the system. See
            `PositionSourceOrigin`.
        position_source_origin_id: Id of the position source origin.
        position_source_type: The channel that reported the position, for
            example email, a chat application (Slack, Teams, WhatsApp) or a
            model prediction. See `PositionSourceType`.
        position_source_type_id: Id of the position source type.
        last_marketed_date: When the operator last marketed the vessel. The
            number of days since this date helps to estimate if the vessel
            is committed or under negotiation.
        latest_updated_date: When the commercial data of the vessel was last
            updated. Shows how recent the data is.
        forecasted_destination_port: Name of the destination port that the
            system predicts.
        forecasted_destination_port_id: Id of the next port that the system
            predicts from the patterns of the vessel.
    """

    open_location: Optional[str] = None
    open_location_taxonomy: Optional[str] = None
    open_location_geo_id: Optional[int] = None
    open_location_taxonomy_id: Optional[int] = None
    open_date_from: Optional[datetime] = None
    open_date_to: Optional[datetime] = None
    availability_state: Optional[str] = None
    availability_state_id: Optional[int] = None
    market_status: Optional[str] = None
    market_status_id: Optional[int] = None
    market_deployment: Optional[str] = None
    market_deployment_id: Optional[int] = None
    position_source_origin: Optional[str] = None
    position_source_origin_id: Optional[int] = None
    position_source_type: Optional[str] = None
    position_source_type_id: Optional[int] = None
    last_marketed_date: Optional[datetime] = None
    latest_updated_date: Optional[datetime] = None
    forecasted_destination_port: Optional[str] = None
    forecasted_destination_port_id: Optional[int] = None


class VoyageDetails(SupplyResponseModel):
    """Voyage state, cargo and recent cargo history of a vessel.

    Attributes:
        voyage_state: The phase of the current voyage, for example ballast
            (empty), laden (with cargo), loading or discharging. See
            `VoyageState`.
        voyage_state_id: Id of the voyage state.
        cargo_type: Name of the current or last cargo type.
        cargo_type_id: Id of the current or last cargo type.
        cargo_quantity: Cargo quantity in metric tonnes.
        charterer: Charterer company name.
        charterer_id: Charterer company id.
        start_port: Name of the start (load) port of the voyage leg.
        start_port_id: Id of the start (load) port of the voyage leg.
        last_voyage_cargo_types: Cargo type names of the previous voyage.
        last_voyage_cargo_type_ids: Cargo type ids of the previous voyage.
        last_cargo_types: Names of the last cargo types, up to 3. The recent
            cargo history of the vessel.
        last_cargo_type_ids: Ids of the last cargo types, up to 3. The recent
            cargo history of the vessel.
    """

    voyage_state: Optional[str] = None
    voyage_state_id: Optional[int] = None
    cargo_type: Optional[str] = None
    cargo_type_id: Optional[int] = None
    cargo_quantity: Optional[int] = None
    charterer: Optional[str] = None
    charterer_id: Optional[int] = None
    start_port: Optional[str] = None
    start_port_id: Optional[int] = None
    last_voyage_cargo_types: Optional[Tuple[str, ...]] = None
    last_voyage_cargo_type_ids: Optional[Tuple[int, ...]] = None
    last_cargo_types: Optional[Tuple[str, ...]] = None
    last_cargo_type_ids: Optional[Tuple[int, ...]] = None


class AisTracking(SupplyResponseModel):
    """AIS position, movement and destination of a vessel.

    Attributes:
        last_movement_date_time_utc: Last time the system detected a
            movement of the vessel, in UTC. Shows if the vessel is
            stationary or underway.
        days_since_latest_ais: Days since the last AIS message of the
            vessel. More than 7 days can mean that the AIS is off or out of
            coverage.
        ais_latitude_average: Average latitude of the day.
        ais_longitude_average: Average longitude of the day.
        ais_draught_average: Average draught of the day, in metres.
        ais_heading_average: Average heading of the day, in degrees.
        ais_speed_average: Average speed of the day in knots. Includes the
            time steaming and the time stationary.
        ais_seagoing_speed_average: Average steaming speed of the day in
            knots. Speeds below 5 knots are not included.
        ais_current_area: Name of the standard area of the AIS position, for
            example US Gulf.
        ais_current_area_id: Id of the standard area of the AIS position.
        ais_closest_location: Name of the location nearest to the AIS
            position.
        ais_closest_location_id: Id of the location nearest to the AIS
            position.
        ais_destination: Name of the destination that the vessel reports on
            AIS.
        ais_destination_taxonomy: Precision level of the AIS destination,
            for example `Port`.
        ais_destination_geo_id: Geo id of the AIS destination. The crew
            enters this destination.
        ais_destination_taxonomy_id: Precision level id of the AIS
            destination. See `LocationTaxonomy`.
        eta_to_ais_destination: ETA to the AIS destination, calculated by
            the system. It is not the ETA that the crew reports.
        miles_to_ais_destination: Distance to the AIS destination in
            nautical miles.
        delays_to_ais_destination: Estimated delays to the AIS destination,
            in hours.
    """

    last_movement_date_time_utc: Optional[datetime] = Field(
        None, alias="lastMovementDateTimeUTC"
    )
    days_since_latest_ais: Optional[float] = None
    ais_latitude_average: Optional[float] = None
    ais_longitude_average: Optional[float] = None
    ais_draught_average: Optional[float] = None
    ais_heading_average: Optional[float] = None
    ais_speed_average: Optional[float] = None
    ais_seagoing_speed_average: Optional[float] = None
    ais_current_area: Optional[str] = None
    ais_current_area_id: Optional[int] = None
    ais_closest_location: Optional[str] = None
    ais_closest_location_id: Optional[int] = None
    ais_destination: Optional[str] = None
    ais_destination_taxonomy: Optional[str] = None
    ais_destination_geo_id: Optional[int] = None
    ais_destination_taxonomy_id: Optional[int] = None
    eta_to_ais_destination: Optional[datetime] = None
    miles_to_ais_destination: Optional[float] = None
    delays_to_ais_destination: Optional[float] = None


class SupplyEta(SupplyResponseModel):
    """The result of one custom ETA calculation for a vessel.

    Attributes:
        basis_port_id: The port of the ETA calculation.
        eta: The estimated time of arrival.
        distance: Distance to the port in nautical miles.
        id: The `id` of the ETA configuration in the request.
        canals: Canals on the route.
    """

    basis_port_id: Optional[int] = None
    eta: Optional[datetime] = None
    distance: Optional[float] = None
    id: Optional[str] = None
    canals: Optional[Tuple[str, ...]] = None


class VesselDetails(SupplyResponseModel):
    """Extra vessel details, returned when live supply includes details.

    Attributes:
        notes: Your company's notes on the vessel.
    """

    notes: Optional[str] = None


class SupplyRecord(SupplyResponseModel):
    """The state of one vessel on one day.

    Attributes:
        day: The snapshot day.
        imo: The vessel's IMO number.
        vessel_class_id: The vessel class.
        vessel_class: The vessel class name.
        commercial_availability: Open location, dates and status.
        voyage_details: Voyage state and cargo.
        ais_tracking: AIS position and destination.
        eta_details: One entry per ETA configuration in the request.
        details: Extra details, only when live supply includes details.
    """

    day: Optional[datetime] = None
    imo: Optional[int] = None
    vessel_class_id: Optional[Union[int, str]] = None
    vessel_class: Optional[str] = None
    commercial_availability: Optional[CommercialAvailability] = None
    voyage_details: Optional[VoyageDetails] = None
    ais_tracking: Optional[AisTracking] = None
    eta_details: Annotated[Tuple[SupplyEta, ...], _EMPTY_IF_NULL] = ()
    details: Optional[VesselDetails] = None


class SupplySnapshot(SupplyResponseModel):
    """Vessel records of one day, from historical or live supply.

    Attributes:
        data: One record per vessel.
        include_details: True when the live request asked for details.
    """

    data: Annotated[Tuple[SupplyRecord, ...], _EMPTY_IF_NULL] = ()
    include_details: bool = Field(False, exclude=True)

    def to_data_frame(self) -> pd.DataFrame:
        """Return the records as a data frame with one row per vessel.

        Returns:
            A data frame. See `Column` for the column names.
        """
        return snapshot_to_data_frame(self)
