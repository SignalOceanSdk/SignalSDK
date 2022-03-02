"""Models instantiated by the voyages api."""
from dataclasses import dataclass
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
    """ """

    imo: int
    vessel_name: str
    purpose: str
    port_name_geos: str
    country_geos: str
    area_name_level0_geos: str
    waiting_time_start: datetime
    waiting_time_end: datetime
    operating_time_star: datetime
    operating_time_end: datetime
    day_date: date
    mode: str
    geo_asset_name: str
    latitude: float
    longitude: float
    arrival_date: datetime
