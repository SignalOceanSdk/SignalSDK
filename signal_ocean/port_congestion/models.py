"""Models that define the schemas of Port Congestion Data."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


class LiveCongestion:
    """Detailed information about Live Congestion.

    Live Congestion describes the current
    situation regarding waiting and operating vessels.

    Attributes:
        imo: The imo of the vessel.
        vessel_name: The name of the vessel.
        area_name_level0_geos: Name of the port's narrow area.
        country_geos: The name of the port's Country.
        geo_asset_name: The name of the port's geo asset.
        port_name_geos: The name of the port.
        arrival_date: The date the vessel arrived at the port.
        Mode: Waiting or Operating
        days_at_port: How many days a vessel is at port.
    """

    imo: int
    vessel_name: str
    area_name_level0_geos: str
    country_geos: str
    geo_asset_name: str
    port_name_geos: str
    arrival_date: date
    Mode: str
    days_at_port: float


class NumberOfVesselsOverTime:
    """Number of vessels time series.

    NumberOfVesselsOverTime provides the number
    of vessels at port point in time.

    Attributes:
        date: Date under consideration.
        number_of_vessels: The number of vessels at
            port during that date.
    """

    date: date
    number_of_vessels: int


class WaitingTimeOverTime:
    """Waiting Time time series.

    WaitingTimeOverTime provides the average
    waiting time of the vessels at port point in time.

    Attributes:
        date: Date under consideration.
        avg_waiting_time: The average
            waiting time that the vessels have been
            waiting at port.
    """

    date: date
    avg_waiting_time: float


class VesselsCongestionData:
    """Basis dataset to calculate Port Congestion.

    Provides daily information for the vessels
    that contribute in port congestion point in time.

    Attributes:
        imo: Unique number for each vessel.
        vessel_name: The name of the vessel.
        purpose: Load or Discharge.
        port_name_geos: The name of the port.
        area_name_level0_geos: The name of the
            narrow area.
        waiting_time_start: Starting point
            of the waiting duration.
        waiting_time_end: Ending point
            of the waiting duration.
        operating_time_start: Starting point
            of the operating duration.
        operating_time_end: The time that
            the operation ended.
        mode: Waiting or Operating
        geo_asset_name: The name of the geo asset
            where the load or discharge took place.
        latitude: Latitude of the geo asset.
        longitude: longitude of the geo asset.
        arrival_date: Arrival date of the vessel.
    """

    imo: int
    vessel_name: str
    purpose: str
    port_name_geos: str
    country_geos: str
    area_name_level0_geos: str
    waiting_time_start: datetime
    waiting_time_end: datetime
    operating_time_start: datetime
    operating_time_end: datetime
    day_date: date
    mode: str
    geo_asset_name: str
    latitude: float
    longitude: float
    arrival_date: datetime


@dataclass(frozen=True)
class PortCongestionTimeSeriesEntry:
    """A Port Congestion API timeseries entry representation.

    Attributes:
        queue (int): The port queue size.
        queue_loading (int): The number of vessels in the queue with
                             Purpose = Loading
        queue_discharging (int): The number of vessels in the queue with
                                 Purpose = Discharging
        arrivals (int): The port arrivals amount.
        departures (int): The port departures amount.
        avg_days_since_arrival (float): Average days since arrival.
        avg_wait_estimate (float): Average waiting time estimate.
        avg_eventual_days_by_departure (float): Average number of total
                                                port days of all vessels
                                                departing on this date
        observation_date (datetime): Corresponding day.
    """

    queue: int
    queue_loading: int
    queue_discharging: int
    arrivals: int
    departures: int
    avg_days_since_arrival: float
    avg_wait_estimate: float
    avg_eventual_days_by_departure: float
    observation_date: datetime


@dataclass(frozen=True)
class PortCongestionQueryResponse:
    """Port Congestion API Query endpoint response model.

    Attributes:
        time_series (list): A list of PortCongestionTimeSeriesEntries
        query_errors (list, optional): A potential list of errors reported
                                       from the endpoint.
    """

    time_series: List[PortCongestionTimeSeriesEntry]
    query_errors: Optional[List[str]] = None
