from datetime import datetime
from typing import Tuple

from signal_ocean.historical_tonnage_list import HistoricalTonnageList, TonnageList, Vessel, \
    IndexLevel, Column
from .create_vessel import create_vessel


def create_tonnage_list(
        date: datetime = datetime.now(),
        vessels: Tuple[Vessel, ...] = None):
    if vessels is None:
        vessels = tuple()
    return TonnageList(date, vessels)


def test_can_be_indexed():
    tonnage_list1 = create_tonnage_list()
    tonnage_list2 = create_tonnage_list()
    htl = HistoricalTonnageList([tonnage_list1, tonnage_list2])

    result = htl[1]

    assert result == tonnage_list2


def test_has_length():
    htl = HistoricalTonnageList((create_tonnage_list(), create_tonnage_list()))

    assert len(htl) == 2


def test_has_multiindex_when_converted_to_data_frame():
    tonnage_list1 = create_tonnage_list(
        datetime(2020, 6, 9, 12),
        (create_vessel(imo=1), create_vessel(imo=2))
    )
    tonnage_list2 = create_tonnage_list(
        datetime(2020, 6, 8, 15),
        (create_vessel(imo=3),)
    )
    htl = HistoricalTonnageList([tonnage_list1, tonnage_list2])

    data_frame = htl.to_data_frame()

    date_values = data_frame.index.get_level_values(IndexLevel.DATE).to_list()
    imo_values = data_frame.index.get_level_values(IndexLevel.IMO).to_list()
    assert date_values == [
        tonnage_list1.date.date(),
        tonnage_list1.date.date(),
        tonnage_list2.date.date()
    ]
    assert imo_values == [1, 2, 3]


def test_contains_vessel_data_when_converted_to_data_frame():
    v = create_vessel()
    htl = HistoricalTonnageList([create_tonnage_list(vessels=(v,))])

    df = htl.to_data_frame()

    assert len(df.index) == 1
    assert df[Column.BREADTH_EXTREME].to_list() == [v.breadth_extreme]
    assert df[Column.COMMERCIAL_OPERATOR].to_list() == [v.commercial_operator]
    assert df[Column.COMMERCIAL_STATUS].to_list() == [v.commercial_status]
    assert df[Column.DEADWEIGHT].to_list() == [v.deadweight]
    assert df[Column.ETA].to_list() == [v.eta]
    assert df[Column.ICE_CLASS].to_list() == [v.ice_class]
    assert df[Column.LATEST_AIS].to_list() == [v.latest_ais]
    assert df[Column.LENGTH_OVERALL].to_list() == [v.length_overall]
    assert df[Column.MARKET_DEPLOYMENT].to_list() == [v.market_deployment]
    assert df[Column.NAME].to_list() == [v.name]
    assert df[Column.OPEN_COUNTRY].to_list() == [v.open_country]
    assert df[Column.OPEN_DATE].to_list() == [v.open_date]
    assert df[Column.OPEN_NARROW_AREA].to_list() == [v.open_narrow_area]
    assert df[Column.OPEN_PORT].to_list() == [v.open_port]
    assert df[Column.OPEN_PREDICTION_ACCURACY].to_list() == [v.open_prediction_accuracy]
    assert df[Column.OPEN_WIDE_AREA].to_list() == [v.open_wide_area]
    assert df[Column.OPERATIONAL_STATUS].to_list() == [v.operational_status]
    assert df[Column.PUSH_TYPE].to_list() == [v.push_type]
    assert df[Column.SUBCLASS].to_list() == [v.subclass]
    assert df[Column.VESSEL_CLASS].to_list() == [v.vessel_class]
    assert df[Column.YEAR_BUILT].to_list() == [v.year_built]
