"""Models that difine the schemas of Port Congestion Data."""
from datetime import datetime, date


class LiveCongestion:
    """Detailed information about Live Congestion.

    Live Congestion describes the current
    situation regarding waiting and operatin vessels.

    Attributes:
        imo: int. The imo of the vessel.
        vessel_name: str. The name of the vessel.
        area_name_level0_geos: str. Name of the port's narrow area.
        country_geos: str. The name of the port's Country.
        geo_asset_name: str. The name of the port's geo asset.
        port_name_geos: str. The name of the port.
        arrival_date: date. The date the vessel arrived at the port.
        Mode: str. Waiting or Operating
        days_at_port: floa. How many days a vessel is at port.
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
        date: date. Date under consideration.
        number_of_vessels: int. The number of vessels at
            port durin that date.
    """

    date: date
    number_of_vessels: int


class WaitingTimeOverTime:
    """Waiting Time time series.

    WaitingTimeOverTime provides the average
    waiting time of the vessels at port point in time.

    Attributes:
        date: date. Date under consideration.
        avg_waiting_time: float. The average
            waiting time that the vessels have been
            waiting at port.
    """

    date: date
    avg_waiting_time: float


class VesselsCongestionData:
    """Basis dataset to calculate Port Congestion.

    Provides daily information for the vessels
    that contribute in port congestion point in time.

    imo: int. Unique number for each vessel.
        vessel_name: str. The name of the vessel
    purpose: str. Load or Discharge
    port_name_geos: str. The name of the port
    area_name_level0_geos: str. The name of the
        narrow area
    waiting_time_start: datetime. Starting point
        of the waiting duration.
    waiting_time_end: datetime. Ending point
        of the waiting duration.
    operating_time_start: datetime. Starting point
        of the operating duration.
    operating_time_end: datetime. The time that
        the operation ended.
    mode: str. Waiting or Operating
    geo_asset_name: str. The name of the geo asset
        where the load or discharge is operated
    latitude: float. Latitude of the geo asset
    longitude: float. longitude of the geo asset
    arrival_date: datetime. Arrival date of the vessel
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
