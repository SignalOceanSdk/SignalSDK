"""Models that difine the schemas of Port Congestion Data."""
from datetime import datetime, date


class LiveCongestion:
    """
    Attributes:
        date: date. The date under consideration.
        number_of_vessels: Int. The vessel of vessels at port.
        avg_waiting_time: float. The average time that the vessels
            have been waiting up until the date under consideration.
    """

    date: date
    number_of_vessels: int
    avg_waiting_time: float


class NumberOfVesselsOverTime:
    """
    Attributes:
        date: date. Date under consideration.
        number_of_vessels: int. The number of vessels at
            port durin that date.
    """

    date: date
    number_of_vessels: int


class WaitingTimeOverTime:
    """
    Attributes:
        date: date. Date under consideration.
        avg_waiting_time: float. The average
            waiting time that the vessels have been
            waiting at port.
    """

    date: date
    avg_waiting_time: float


class VesselsCongestionData:
    """
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
