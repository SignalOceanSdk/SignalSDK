# noqa: D100

from typing import Dict, List, Any

from .._internals import IterableConstants
from .vessel import Vessel


def _pit_col(name: str) -> str:
    return f"{name}_point_in_time"


_data_types: Dict[str, str] = {}


def _category(name: str) -> str:
    _data_types[name] = "category"
    return name


class Column(metaclass=IterableConstants):
    """Contains constants for data frame column names."""

    NAME = "name"
    VESSEL_CLASS = _category("vessel_class")
    ICE_CLASS = _category("ice_class")
    YEAR_BUILT = "year_built"
    DEADWEIGHT = "deadweight"
    LENGTH_OVERALL = "length_overall"
    BREADTH_EXTREME = "breadth_extreme"
    SUBCLASS = _category("subclass")
    MARKET_DEPLOYMENT = _category(_pit_col("market_deployment"))
    PUSH_TYPE = _category(_pit_col("push_type"))
    OPEN_PORT = _category(_pit_col("open_port"))
    OPEN_DATE = _pit_col("open_date")
    OPERATIONAL_STATUS = _category(_pit_col("operational_status"))
    COMMERCIAL_OPERATOR = _category(_pit_col("commercial_operator"))
    COMMERCIAL_STATUS = _category(_pit_col("commercial_status"))
    ETA = _pit_col("eta")
    LATEST_AIS = _pit_col("latest_ais")
    OPEN_PREDICTION_ACCURACY = _category(_pit_col("open_prediction_accuracy"))
    OPEN_COUNTRY = _category(_pit_col("open_country"))
    OPEN_NARROW_AREA = _category(_pit_col("open_narrow_area"))
    OPEN_WIDE_AREA = _category(_pit_col("open_wide_area"))
    AVAILABILITY_PORT_TYPE = _category(_pit_col("availability_port_type"))
    AVAILABILITY_DATE_TYPE = _category(_pit_col("availability_date_type"))

    @staticmethod
    def _create_row(vessel: Vessel) -> List[Any]:
        return [
            vessel.name,
            vessel.vessel_class,
            vessel.ice_class,
            vessel.year_built,
            vessel.deadweight,
            vessel.length_overall,
            vessel.breadth_extreme,
            vessel.subclass,
            vessel.market_deployment,
            vessel.push_type,
            vessel.open_port,
            vessel.open_date,
            vessel.operational_status,
            vessel.commercial_operator,
            vessel.commercial_status,
            vessel.eta,
            vessel.latest_ais,
            vessel.open_prediction_accuracy,
            vessel.open_country,
            vessel.open_narrow_area,
            vessel.open_wide_area,
            vessel.availability_port_type,
            vessel.availability_date_type
        ]

    @staticmethod
    def _get_data_types() -> Dict[str, str]:
        return _data_types
