"""Utilities for working with tonnage list data frames."""

from datetime import datetime
from typing import Dict, Optional, Tuple

from .._internals import IterableConstants


def _pit_col(name: str) -> str:
    return f"{name}_point_in_time"


_data_types: Dict[str, str] = {}


def _category(name: str) -> str:
    _data_types[name] = "category"
    return name


DataFrameRow = Tuple[
    str,
    str,
    Optional[str],
    int,
    int,
    float,
    int,
    str,
    str,
    str,
    int,
    str,
    Optional[datetime],
    str,
    int,
    str,
    str,
    Optional[datetime],
    Optional[datetime],
    str,
    Optional[str],
    Optional[str],
    Optional[str],
    str,
    str,
    str,
    int,
    str,
    bool
]


class Column(metaclass=IterableConstants):
    """Contains constants for data frame column names."""

    NAME = "name"
    """The vessel's name."""

    VESSEL_CLASS = _category("vessel_class")
    """Name of the vessel class the vessel is categorized as."""

    ICE_CLASS = _category("ice_class")
    """The vessel's ice class."""

    YEAR_BUILT = "year_built"
    """The year the vessel has been built."""

    DEADWEIGHT = "deadweight"
    """The vessel's deadweight."""

    LENGTH_OVERALL = "length_overall"
    """The vessel's length overall."""

    BREADTH_EXTREME = "breadth_extreme"
    """The vessel's breadth extreme."""

    SUBCLASS = _category("subclass")
    """The vessel's subclass. See the `VesselSubclass` class for available
    values."""

    MARKET_DEPLOYMENT = _category(_pit_col("market_deployment"))
    """Market deployment of the vessel at the tonnage lists' point in time. See
    the `MarketDeployment` class for available values."""

    PUSH_TYPE = _category(_pit_col("push_type"))
    """Push type of the vessel at the tonnage lists' point in time. See the
    `PushType` class for available values."""

    OPEN_PORT_ID = _category(_pit_col("open_port_id"))
    """The vessel's open port id at the tonnage lists' point in time."""

    OPEN_PORT = _category(_pit_col("open_port"))
    """The vessel's open port name at the tonnage lists' point in time."""

    OPEN_DATE = _pit_col("open_date")
    """The vessel's open date at the tonnage lists' point in time."""

    OPERATIONAL_STATUS = _category(_pit_col("operational_status"))
    """Operational status of the vessel at the tonnage lists' point in time.
    See the `OperationalStatus` class for available values."""

    COMMERCIAL_OPERATOR_ID = _category(_pit_col("commercial_operator_id"))
    """The vessel's commercial operator id at the tonnage lists' point in
    time."""

    COMMERCIAL_OPERATOR = _category(_pit_col("commercial_operator"))
    """The vessel's commercial operator at the tonnage lists' point in time."""

    COMMERCIAL_STATUS = _category(_pit_col("commercial_status"))
    """Commercial status of the vessel at the tonnage lists' point in time. See
    the `CommercialStatus` class for available values."""

    ETA = _pit_col("eta")
    """Estimated time of arrival at the tonnage lists' point in time."""

    LATEST_AIS = _pit_col("latest_ais")
    """Timestamp of the vessel's latest AIS information at the tonnage lists'
    point in time."""

    OPEN_PREDICTION_ACCURACY = _category(_pit_col("open_prediction_accuracy"))
    """How accurate, in terms of location taxonomy, is the vessel's open
    prediction at the tonnage lists' point in time. See the `LocationTaxonomy`
    class for available values."""

    OPEN_COUNTRY = _category(_pit_col("open_country"))
    """The country at which the vessel opens."""

    OPEN_NARROW_AREA = _category(_pit_col("open_narrow_area"))
    """The narrow geographical area at which the vessel opens."""

    OPEN_WIDE_AREA = _category(_pit_col("open_wide_area"))
    """The wide geographical area at which the vessel opens."""

    AVAILABILITY_PORT_TYPE = _category(_pit_col("availability_port_type"))
    """Prediction source of the vessel's open port at the tonnage lists' point
    in time. See the `SourceType` class for possible values."""

    AVAILABILITY_DATE_TYPE = _category(_pit_col("availability_date_type"))
    """Prediction source of the vessel's open date at the tonnage lists' point
    in time. See the `SourceType` class for possible values."""

    FIXTURE_TYPE = _category(_pit_col("fixture_type"))
    """Fixture type. One of Scraped, Manual, Implied"""

    CURRENT_VESSEL_SUB_TYPE_ID = _category(
                                    _pit_col("current_vessel_sub_type_id")
                                          )
    """Current vessel sub type Id"""

    CURRENT_VESSEL_SUB_TYPE = _category(_pit_col("current_vessel_sub_type"))
    """One of: -1: Unknown, 1: Dirty, 2: Clean"""

    WILLING_TO_SWITCH_CURRENT_VESSEL_SUB_TYPE = _pit_col(
                    "willing_to_switch_current_vessel_sub_type"
                                                         )
    """If the vessel is willing to compete on a different vessel subclass
    category or not"""

    @staticmethod
    def _create_row(
        name: str,
        vessel_class: str,
        ice_class: Optional[str],
        year_built: int,
        deadweight: int,
        length_overall: float,
        breadth_extreme: int,
        subclass: str,
        market_deployment: str,
        push_type: str,
        open_port_id: int,
        open_port: str,
        open_date: Optional[datetime],
        operational_status: str,
        commercial_operator_id: int,
        commercial_operator: str,
        commercial_status: str,
        eta: Optional[datetime],
        latest_ais: Optional[datetime],
        open_prediction_accuracy: str,
        open_country: Optional[str],
        open_narrow_area: Optional[str],
        open_wide_area: Optional[str],
        availability_port_type: str,
        availability_date_type: str,
        fixture_type: str,
        current_vessel_sub_type_id: int,
        current_vessel_sub_type: str,
        willing_to_switch_current_vessel_sub_type: bool,
    ) -> DataFrameRow:
        return (
            name,
            vessel_class,
            ice_class,
            year_built,
            deadweight,
            length_overall,
            breadth_extreme,
            subclass,
            market_deployment,
            push_type,
            open_port_id,
            open_port,
            open_date,
            operational_status,
            commercial_operator_id,
            commercial_operator,
            commercial_status,
            eta,
            latest_ais,
            open_prediction_accuracy,
            open_country,
            open_narrow_area,
            open_wide_area,
            availability_port_type,
            availability_date_type,
            fixture_type,
            current_vessel_sub_type_id,
            current_vessel_sub_type,
            willing_to_switch_current_vessel_sub_type
        )

    @staticmethod
    def _get_data_types() -> Dict[str, str]:
        return _data_types


class IndexLevel(metaclass=IterableConstants):
    """Contains constants for available data frame index levels."""

    DATE = "date"
    """The point in time at which the data was captured."""

    IMO = "imo"
    """The vessel's IMO number."""
