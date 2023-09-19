"""Port Congestion."""
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional, Tuple, List, cast
from strictly_typed_pandas.dataset import DataSet
from functools import reduce

from signal_ocean import Connection
from signal_ocean.port_congestion.port_congestion_api import PortCongestionAPI
from signal_ocean.voyages import VoyagesAPI
from signal_ocean.voyages.models import (
    Voyage,
    VoyageEvent,
    VoyageEventDetail,
    VoyageGeo,
    VoyagesFlat,
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
        """Initializes PortCongestion.

        Args:
            connection: API connection configuration. If not provided, the
                default connection method is used.
        """
        self.__connection = connection or Connection()
        self._port_congestion_api = PortCongestionAPI(self.__connection)

    def _get_voyages_data(
        self, voyages_start_date: date, vessel_class_id: int,
    ) -> Tuple[
        DataSet[Voyage],
        DataSet[VoyageEvent],
        DataSet[VoyageEventDetail],
        DataSet[VoyageGeo],
    ]:
        """Get Voyages Data to calculate port congestion.

        Args:
            voyages_start_date: We retrieve voyages after that date.
            vessel_class_id: We retrieve the voyages of the specific
                vessel class id.

        Returns:
            Voyages, Events, Events Details and Geos.
        """
        voyages_api = VoyagesAPI(self.__connection)

        voyages_flat = voyages_api.get_voyages_flat(
            vessel_class_id=vessel_class_id, date_from=voyages_start_date
        )
        voyages_flat = cast(VoyagesFlat, voyages_flat)

        voyages_df = cast(
            DataSet[Voyage],
            pd.DataFrame(
                v.__dict__  # type: ignore
                for v in cast(Tuple[Voyage, ...], voyages_flat.voyages)
            ),
        )
        events_df = cast(
            DataSet[VoyageEvent],
            pd.DataFrame(
                v.__dict__  # type: ignore
                for v in cast(Tuple[VoyageEvent, ...], voyages_flat.events)
            ),
        )
        events_details_df = cast(
            DataSet[VoyageEventDetail],
            pd.DataFrame(
                v.__dict__  # type: ignore
                for v in cast(
                    Tuple[VoyageEventDetail, ...], voyages_flat.event_details
                )
            ),
        )
        geos_df = cast(
            DataSet[VoyageGeo],
            pd.DataFrame(
                v.__dict__  # type: ignore
                for v in cast(Tuple[VoyageGeo, ...], voyages_flat.geos)
            ).drop_duplicates(),
        )

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
        """Preprocess Voyages to get Port Congestion data.

        Args:
            voyages_df: Voyages DataFrame.
            events_df: Events DataFrame.
            events_details_df: EventDetails DataFrame.
            geos_df: Geos DataFrame
            congestion_start_date: starting point of port
                congestion calculation
            ports: ports for which the congestion will
                be calculated.
            areas: areas for which the congestion will
                be calculated.

        Returns:
            VesselsCongestionData.
        """
        left_merge_keys = iter(["id", "id_ev", "geo_asset_id_ev"])
        right_merge_keys = iter(["voyage_id", "event_id", "id"])
        suffixes = iter([("_voy", "_ev"), ("_ev", "_det"), ("", "_geos")])

        voyages_extd = cast(
            pd.DataFrame,
            reduce(
                lambda left, right: pd.merge(
                    left,  # type: ignore
                    right,  # type: ignore
                    how="left",
                    left_on=next(left_merge_keys, None),
                    right_on=next(right_merge_keys, None),
                    suffixes=next(suffixes, (None,)),
                ),
                [voyages_df, events_df, events_details_df, geos_df],
            ),
        )

        _filter = pd.Series([True] * voyages_extd.shape[0])

        if ports and not areas:
            ports_filter = voyages_extd.port_name_geos.isin(ports)
            _filter = _filter & ports_filter
        elif areas and not ports:
            areas_filter = voyages_extd.area_name_level0_geos.isin(areas)
            _filter = _filter & areas_filter
        elif areas and ports:
            areas_ports_filter = (
                voyages_extd.area_name_level0_geos.isin(areas)
            ) | (voyages_extd.port_name_geos.isin(ports))
            _filter = _filter & areas_ports_filter
        else:
            pass

        voyages_extd = voyages_extd[
            (voyages_extd["purpose"].isin(["Load", "Discharge"]))
            & (voyages_extd["event_detail_type"] != "StS")
            & _filter
        ].copy()

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

        vessels_congestion_data_datetimetz = vessels_congestion_data.\
            select_dtypes("datetimetz")
        vessels_congestion_data[
            vessels_congestion_data_datetimetz.columns
        ] = vessels_congestion_data_datetimetz.apply(
            lambda x: x.dt.tz_convert(None), axis=0
        )

        vessels_congestion_data = cast(
            DataSet[VesselsCongestionData],
            (
                vessels_congestion_data[
                    vessels_congestion_data.day_date.dt.date.between(
                        congestion_start_date, date.today()
                    )
                ]
            )[wanted_columns]
            .copy()
            .reset_index(drop=True),
        )

        return vessels_congestion_data

    def _calculate_number_of_vessels_over_time(
        self, vessels_congestion_data: DataSet[VesselsCongestionData]
    ) -> DataSet[NumberOfVesselsOverTime]:
        """Generate number of vessels time series.

        Args:
            VesselsCongestionData: The Dataset over which
                port congestion will be calculated.

        Returns:
            NumberOfVesselsOverTime.
        """
        num_of_vessels_time_series = cast(
            DataSet[NumberOfVesselsOverTime],
            (
                vessels_congestion_data.groupby("day_date")["imo"]
                .nunique()
                .reset_index()
            ),
        )

        num_of_vessels_time_series.columns = ["date", "vessels"]  # type:ignore

        return num_of_vessels_time_series

    def _get_waiting_time_over_time(
        self,
        congestion_start_date: date,
        vessel_class_id: int,
        ports: Optional[List[str]] = None,
        areas: Optional[List[str]] = None,
    ) -> DataSet[WaitingTimeOverTime]:
        """Generate waiting time time series.

        Args:
            VesselsCongestionData: The Dataset over which
                port congestion will be calculated.

        Raises:
            RuntimeError: In case of Port Congestion API call failure.

        Returns:
            WaitingTimeOverTime.
        """
        try:
            ts_df = pd.DataFrame(
                self._port_congestion_api.query_port_congestion(
                    date_from=congestion_start_date,
                    vessel_class_ids=[vessel_class_id],
                    ports=ports,
                    level_0_areas=areas,
                )
            )
        except RuntimeError as exc:
            raise exc

        waiting_time_df = (
            ts_df.rename(
                columns={
                    "observation_date": "date",
                    "avg_wait_estimate": "avg_waiting_time",
                }
            )
            .groupby("date")
            .mean()
            .reset_index()
            .set_index("date")
        )
        waiting_time_df.avg_waiting_time = waiting_time_df.\
            avg_waiting_time.round(1)
        waiting_time_df.index = cast(
            pd.Index, pd.to_datetime(waiting_time_df.index).tz_convert(None)
        )
        waiting_time_df = waiting_time_df.reset_index()

        return cast(
            DataSet[WaitingTimeOverTime],
            waiting_time_df[["date", "avg_waiting_time"]],
        )

    def _calculate_live_port_congestion(
        self, vessels_congestion_data: DataSet[VesselsCongestionData]
    ) -> DataSet[LiveCongestion]:
        """Generate live port congestion DataFrame.

        Args:
            VesselsCongestionData: The Dataset over which
                port congestion will be calculated.

        Returns:
            LiveCongestion.
        """
        vessels_at_port_df = vessels_congestion_data[
            (vessels_congestion_data.day_date.dt.date == date.today())
        ].copy()

        vessels_at_port_df["days_at_port"] = (
            vessels_at_port_df.day_date - vessels_at_port_df["arrival_date"]
        ).dt.total_seconds() / (60 * 60 * 24.0)

        vessels_at_port_df.loc[
            vessels_at_port_df.days_at_port < 0, "days_at_port"
        ] = None
        return cast(
            DataSet[LiveCongestion], vessels_at_port_df.reset_index(drop=True)
        )

    def get_port_congestion(
        self,
        congestion_start_date: date,
        vessel_class_id: int,
        ports: Optional[List[str]] = None,
        areas: Optional[List[str]] = None,
    ) -> Tuple[
        DataSet[NumberOfVesselsOverTime],
        DataSet[WaitingTimeOverTime],
        DataSet[LiveCongestion],
        DataSet[VesselsCongestionData],
    ]:
        """Get port congestion data.

        Args:
            congestion_start_date: starting point of port
                congestion calculation
            ports: ports for which the congestion will
                be calculated.
            areas: areas for which the congestion will
                be calculated.

        Returns:
            NumberOfVesselsOverTime,
            WaitingTimeOverTime,
            LiveCongestion,
            VesselsCongestionData.
        """
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

        num_of_vessels_over_time = self._calculate_number_of_vessels_over_time(
            vessels_congestion_data
        )

        try:
            waiting_time_over_time = self._get_waiting_time_over_time(
                congestion_start_date, vessel_class_id, ports, areas
            )
        except RuntimeError:
            waiting_time_over_time = cast(
                DataSet[WaitingTimeOverTime],
                {"date": congestion_start_date, "avg_waiting_time": 0.0},
            )

        live_port_congestion = self._calculate_live_port_congestion(
            vessels_congestion_data
        )

        return (
            num_of_vessels_over_time,
            waiting_time_over_time,
            live_port_congestion,
            vessels_congestion_data,
        )
