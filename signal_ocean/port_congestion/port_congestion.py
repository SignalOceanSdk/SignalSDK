""" Port Congestion"""
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional, Tuple, List
from strictly_typed_pandas import DataSet, IndexedDataSet
from urllib.parse import urljoin, urlencode
from functools import reduce

from signal_ocean import Connection
from signal_ocean.voyages import VoyagesAPI
from signal_ocean.voyages.models import (
    Voyage,
    VoyageEvent,
    VoyageEventDetail,
    VoyageGeo,
)
from signal_ocean.port_congestion.models import (
    LiveCongestion,
    NumberOfVesselsOverTime,
    WaitingTimeOverTime,
    VesselsCongestionData,
)

import numpy as np
import pandas as pd


class PortCongestion:
    """Represents Signal's Port Congestion."""

    def __init__(self, connection: Optional[Connection] = None):
        """ """
        self.__connection = connection or Connection()

    def _get_voyages_data(
        self,
        voyages_start_date: date,
        vessel_class_id: int,
    ) -> Tuple[
        DataSet[Voyage],
        DataSet[VoyageEvent],
        DataSet[VoyageEventDetail],
        DataSet[VoyageGeo],
    ]:

        voyages_api = VoyagesAPI(self.__connection)

        voyages_flat = voyages_api.get_voyages_flat(
            vessel_class_id=vessel_class_id, date_from=voyages_start_date
        )

        voyages_df = pd.DataFrame(v.__dict__ for v in voyages_flat.voyages)
        events_df = pd.DataFrame(v.__dict__ for v in voyages_flat.events)
        events_details_df = pd.DataFrame(
            v.__dict__ for v in voyages_flat.event_details
        )
        geos_df = pd.DataFrame(
            v.__dict__ for v in voyages_flat.geos
        ).drop_duplicates()

        return (
            voyages_df,
            events_df,
            events_details_df,
            geos_df,
        )

    def _preprocess_voyages_data(
        self,
        voyages_df: DataSet[Voyage],
        events_df: DataSet[VoyageEvent],
        events_details_df: DataSet[VoyageEventDetail],
        geos_df: DataSet[VoyageGeo],
        congestion_start_date: date,
        ports: Optional[List[str]] = None,
        areas: Optional[List[str]] = None,
    ) -> DataSet[VesselsCongestionData]:
        """ """

        left_merge_keys = iter(["id", "id_ev", "geo_asset_id_ev"])
        right_merge_keys = iter(["voyage_id", "event_id", "id"])
        suffixes = iter([("_voy", "_ev"), ("_ev", "_det"), ("", "_geos")])

        voyages_extd = reduce(
            lambda left, right: pd.merge(
                left,
                right,
                how="left",
                left_on=next(left_merge_keys, None),
                right_on=next(right_merge_keys, None),
                suffixes=next(suffixes, None),
            ),
            [voyages_df, events_df, events_details_df, geos_df],
        )

        ports_filter = pd.Series([True] * voyages_extd.shape[0])
        areas_filter = pd.Series([True] * voyages_extd.shape[0])

        if ports:
            ports_filter = (
                voyages_extd.port_name_geos.isin(ports)
            )
        if areas:
            areas_filter = (
                voyages_extd.area_name_level0_geos.isin(areas)
            )

        final_filter = (ports_filter & areas_filter)

        voyages_extd = voyages_extd[
            (voyages_extd["purpose"].isin(["Load", "Discharge"]))
            & (voyages_extd["event_detail_type"] != "StS")
            & final_filter
        ].copy()

        """ Port Congestion calculation takes into account also 
            stopped vessels outside the port/anchorage limits using 
            the forecasted part of the voyage (mainly driven from AIS).  
            This is achieved by 'connecting' future(predicted) port calls 
            with their previous stops, given that the stops ended during 
            the last 24 hours from the beginnning of the port calls.  
            The above results to new extended port calls that span from 
            previous stop arrival date to future portcall sailing date.
        """
        future_portcalls = events_df.loc[
            (events_df["purpose"].isin(["Load", "Discharge"]))
            & (events_df["event_horizon"] == "Future")
        ]

        stops = events_df.loc[(events_df["purpose"] == "Stop")]

        future_portcalls_extd = future_portcalls.merge(
            stops,
            how="inner",
            left_on="voyage_id",
            right_on="voyage_id",
            suffixes=("_fportcalls", "_stops"),
        )

        future_portcalls_extd["stop_portcall_diff"] = (
            (
                future_portcalls_extd["arrival_date_fportcalls"]
                - future_portcalls_extd["sailing_date_stops"]
            ).dt.total_seconds()
        ) / 3600

        future_portcalls_extd = future_portcalls_extd.loc[
            future_portcalls_extd["stop_portcall_diff"] <= 24
        ]

        future_portcalls_extd = (
            future_portcalls_extd.sort_values("sailing_date_stops")
            .groupby("voyage_id")
            .tail(1)
        )

        voyages_final_df = voyages_extd.merge(
            future_portcalls_extd,
            how="outer",
            left_on=["id_voy", "id_ev"],
            right_on=["voyage_id", "id_fportcalls"],
            suffixes=("_connected", "_portcalls"),
            indicator="Exist",
        )

        voyages_final_df = voyages_final_df[
            voyages_final_df.Exist != "right_only"
        ].copy()

        """ # Define Waiting/Operating time for every vessel

            The date range between start_time_of_operation and 
            end_time_of_operation(sailing date) will be marked as Operating, 
            and the rest of the days inside each port call 
            are going to be marked as waiting.  

            ## Waiting Time

            We will split the port calls into 4 categories whose 
            waiting interval calculation is differentiated.  
            For each category start/end time 
            of the waiting interval is calculated as follows:  
            * **Historical Port Calls with start time of operation** : 
                * waiting_time_start -> event arrival date
                * waiting_time_end -> one day prior to the start time of operation
            * **Historical Port Calls without start time of operation** :    
            (Note) A historical port call may lack the attribute start 
            time of operation due to low ais density during the port call.
                * waiting_time_start -> event arrival date
                * waiting_time_end -> event detail sailing date 
            * **Current Port Calls without start time of operation** :    
            (Note) A Current port call may also have 
            event_horizon = 'Future' due to missing AIS data.
                * waiting_time_start -> event arrival date
                * waiting_time_end -> event sailing date  
            * **Extended Port Calls** :    
            (Note) A Current port call may also have 
            event_horizon = 'Future' due to missing AIS data.
                * waiting_time_start -> arrival date of previous stop
                * waiting_time_end -> event sailing date

            ## Operating Time

            The operating time interval is simply calculated by 
            taking as operating_time_start the start time of operation 
            and as operating_time_end the end time of operation.  
            In cases that later is not available 
            the event sailing date is used instead.
        """
        hist_port_calls_with_start_time_of_operation = (
            voyages_final_df.start_time_of_operation.notna()
        )

        hist_port_calls_without_start_time_of_operation = (
            voyages_final_df.start_time_of_operation.isna()
        ) & (voyages_final_df.event_horizon == "Historical")

        current_port_calls_without_start_time_of_operation = (
            voyages_final_df.start_time_of_operation.isna()
        ) & (voyages_final_df.event_horizon.isin(["Current", "Future"]))

        port_calls_merged_with_previous_stops = (
            voyages_final_df.Exist == "both"
        )

        voyages_final_df.loc[
            hist_port_calls_with_start_time_of_operation
            | hist_port_calls_without_start_time_of_operation
            | current_port_calls_without_start_time_of_operation,
            "waiting_time_start",
        ] = voyages_final_df[
            hist_port_calls_with_start_time_of_operation
            | hist_port_calls_without_start_time_of_operation
            | current_port_calls_without_start_time_of_operation
        ].arrival_date_ev

        voyages_final_df.loc[
            port_calls_merged_with_previous_stops, "waiting_time_start"
        ] = voyages_final_df[
            port_calls_merged_with_previous_stops
        ].arrival_date_stops

        voyages_final_df.loc[
            hist_port_calls_with_start_time_of_operation, "waiting_time_end"
        ] = voyages_final_df[
            hist_port_calls_with_start_time_of_operation
        ].start_time_of_operation.apply(
            lambda x: datetime.combine(x, datetime.min.time())
            - timedelta(minutes=1)
        )

        voyages_final_df.loc[
            hist_port_calls_without_start_time_of_operation, "waiting_time_end"
        ] = voyages_final_df[
            hist_port_calls_without_start_time_of_operation
        ].sailing_date_det

        voyages_final_df.loc[
            current_port_calls_without_start_time_of_operation,
            "waiting_time_end",
        ] = voyages_final_df[
            current_port_calls_without_start_time_of_operation
        ].sailing_date_ev

        voyages_final_df.loc[
            port_calls_merged_with_previous_stops, "waiting_time_end"
        ] = voyages_final_df[
            port_calls_merged_with_previous_stops
        ].sailing_date_fportcalls

        voyages_final_df.loc[
            hist_port_calls_with_start_time_of_operation,
            "operating_time_start",
        ] = voyages_final_df[
            hist_port_calls_with_start_time_of_operation
        ].start_time_of_operation

        voyages_final_df.loc[
            hist_port_calls_with_start_time_of_operation
            & (voyages_final_df.end_time_of_operation.notna()),
            "operating_time_end",
        ] = voyages_final_df[
            hist_port_calls_with_start_time_of_operation
            & (voyages_final_df.end_time_of_operation.notna())
        ].end_time_of_operation

        voyages_final_df.loc[
            hist_port_calls_with_start_time_of_operation
            & (voyages_final_df.end_time_of_operation.isna()),
            "operating_time_end",
        ] = voyages_final_df[
            hist_port_calls_with_start_time_of_operation
            & (voyages_final_df.end_time_of_operation.isna())
        ].sailing_date_ev

        voyages_final_df["waiting_duration"] = voyages_final_df.apply(
            lambda row: pd.date_range(
                row.waiting_time_start.date(), row.waiting_time_end.date()
            ),
            axis=1,
        )

        voyages_final_df["operating_duration"] = voyages_final_df.apply(
            lambda row: pd.date_range(
                row.operating_time_start.date(), row.operating_time_end.date()
            )
            if not pd.isnull(row.operating_time_start)
            else [],
            axis=1,
        )

        mapping_dict = {
            "geo_asset_name": [
                "geo_asset_name_fportcalls",
                "geo_asset_name_ev",
            ],
            "geo_asset_id": ["geo_asset_id_fportcalls", "geo_asset_id_ev"],
            "purpose": ["purpose_fportcalls", "purpose"],
            "latitude": ["latitude_fportcalls", "latitude_ev"],
            "longitude": ["longitude_fportcalls", "longitude_ev"],
            "port_name": ["port_name_fportcalls", "port_name_geos"],
            "arrival_date": ["arrival_date_stops", "arrival_date_ev"],
        }

        conditions = [
            (voyages_final_df["Exist"] == "both"),
            (voyages_final_df["Exist"] != "both"),
        ]
        for key, value in mapping_dict.items():
            actions = [voyages_final_df[value[0]], voyages_final_df[value[1]]]
            voyages_final_df[key] = np.select(
                conditions, actions, default=actions[0]
            )

        vessels_congestion_data = pd.concat(
            [
                (
                    voyages_final_df.explode("operating_duration")
                    .rename({"operating_duration": "day_date"}, axis="columns")
                    .assign(mode="Operating")
                ),
                (
                    voyages_final_df.explode("waiting_duration")
                    .rename({"waiting_duration": "day_date"}, axis="columns")
                    .assign(mode="Waiting")
                ),
            ],
            ignore_index=True,
        ).drop_duplicates(subset=["imo", "day_date"], keep="first")

        wanted_columns = [
            "imo",
            "vessel_name",
            "purpose",
            "port_name_geos",
            "country_geos",
            "area_name_level0_geos",
            "waiting_time_start",
            "waiting_time_end",
            "operating_time_start",
            "operating_time_end",
            "day_date",
            "mode",
            "geo_asset_name",
            "latitude",
            "longitude",
            "arrival_date",
        ]

        vessels_congestion_data_datetimetz = (
            vessels_congestion_data.select_dtypes("datetimetz")
        )
        vessels_congestion_data[
            vessels_congestion_data_datetimetz.columns
        ] = vessels_congestion_data_datetimetz.apply(
            lambda x: x.dt.tz_convert(None), axis=0
        )

        vessels_congestion_data = (
            vessels_congestion_data[
                vessels_congestion_data.day_date.dt.date.between(
                    congestion_start_date, date.today()
                )
            ]
        )[wanted_columns].copy()

        return vessels_congestion_data

    def _calculate_number_of_vessels_over_time(
        self, vessels_congestion_data: DataSet[VesselsCongestionData]
    ) -> DataSet[NumberOfVesselsOverTime]:
        num_of_vessels_time_series = (
            vessels_congestion_data.groupby("day_date")["imo"]
            .nunique()
            .reset_index()
        )
        num_of_vessels_time_series.columns = ["date", "vessels"]

        return num_of_vessels_time_series

    def _calculate_waiting_time_over_time(
        self, vessels_congestion_data: DataSet[VesselsCongestionData]
    ) -> DataSet[WaitingTimeOverTime]:
        """ """
        waiting_vessels = vessels_congestion_data[
            (vessels_congestion_data["mode"] == "Waiting")
            & (
                vessels_congestion_data.waiting_time_start.dt.date
                != vessels_congestion_data.day_date.dt.date
            )
        ].copy()

        waiting_vessels["waiting_time"] = (
            waiting_vessels["day_date"]  # .dt.tz_localize(None)
            - waiting_vessels["waiting_time_start"]  # .dt.tz_localize(None)
        ).dt.total_seconds() / (60 * 60 * 24.0)

        waiting_time_df = (
            waiting_vessels[
                (waiting_vessels.waiting_time < 60)
                & (waiting_vessels.day_date.dt.date != date.today())
            ]
            .groupby("day_date")["waiting_time"]
            .mean()
            .reset_index()
            .rename(columns={"waiting_time": "avg_waiting_time"})
            .set_index("day_date")
        )

        waiting_time_df.avg_waiting_time = (
            waiting_time_df.avg_waiting_time.round(1)
        )

        all_days = pd.date_range(
            waiting_time_df.index.min(), waiting_time_df.index.max(), freq="D"
        )
        waiting_time_df = waiting_time_df.reindex(all_days)

        return waiting_time_df

    def _calculate_live_port_congestion(
        self, vessels_congestion_data: DataSet[VesselsCongestionData]
    ) -> DataSet[LiveCongestion]:
        vessels_at_port_df = vessels_congestion_data[
            (vessels_congestion_data.day_date.dt.date == date.today())
        ].copy()

        vessels_at_port_df["days_at_port"] = (
            vessels_at_port_df.day_date - vessels_at_port_df["arrival_date"]
        ).dt.total_seconds() / (60 * 60 * 24.0)

        vessels_at_port_df.loc[
            vessels_at_port_df.days_at_port < 0, "days_at_port"
        ] = None
        return vessels_at_port_df

    def get_port_congestion(
        self,
        congestion_start_date: datetime,
        vessel_class_id: int,
        ports: Optional[List[str]] = None,
        areas: Optional[List[str]] = None,
    ) -> Tuple[
        DataSet[NumberOfVesselsOverTime],
        DataSet[WaitingTimeOverTime],
        DataSet[LiveCongestion],
        DataSet[VesselsCongestionData],
    ]:
        voyages_start_date = congestion_start_date - relativedelta(months=4)

        (
            voyages_df,
            events_df,
            events_details_df,
            geos_df,
        ) = self._get_voyages_data(voyages_start_date, vessel_class_id)

        vessels_congestion_data = self._preprocess_voyages_data(
            voyages_df,
            events_df,
            events_details_df,
            geos_df,
            congestion_start_date,
            ports,
            areas,
        )

        number_of_vessels_over_time = (
            self._calculate_number_of_vessels_over_time(
                vessels_congestion_data
            )
        )

        waiting_time_over_time = self._calculate_waiting_time_over_time(
            vessels_congestion_data
        )

        live_port_congestion = self._calculate_live_port_congestion(
            vessels_congestion_data
        )

        return (
            number_of_vessels_over_time,
            waiting_time_over_time,
            live_port_congestion,
            vessels_congestion_data,
        )
