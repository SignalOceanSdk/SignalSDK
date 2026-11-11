"""Response models of the Supply API.

Attribute names are the API response names in snake_case.
"""
from datetime import datetime
from typing import Any, Optional, Tuple, Union

from pydantic import BeforeValidator, Field
from typing_extensions import Annotated

from ._base import SupplyResponseModel


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


class CommercialAvailability(SupplyResponseModel):
    """Open location, open dates and commercial status of a vessel."""

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
    """Voyage state, cargo and recent cargo history of a vessel."""

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
    """AIS position, movement and destination of a vessel."""

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
