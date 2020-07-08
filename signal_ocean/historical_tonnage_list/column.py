from .._internals import IterableConstants
from .vessel import Vessel


def _pit_col(name: str) -> str:
    return f'{name}_point_in_time'


class Column(metaclass=IterableConstants):
    NAME = 'name'
    VESSEL_CLASS = 'vessel_class'
    ICE_CLASS = 'ice_class'
    YEAR_BUILT = 'year_built'
    DEADWEIGHT = 'deadweight'
    LENGTH_OVERALL = 'length_overall'
    BREADTH_EXTREME = 'breadth_extreme'
    MARKET_DEPLOYMENT = _pit_col('market_deployment')
    PUSH_TYPE = _pit_col('push_type')
    OPEN_PORT = _pit_col('open_port')
    OPEN_DATE = _pit_col('open_date')
    OPERATIONAL_STATUS = _pit_col('operational_status')
    COMMERCIAL_OPERATOR = _pit_col('commercial_operator')
    COMMERCIAL_STATUS = _pit_col('commercial_status')
    ETA = _pit_col('eta')
    LAST_FIXED = _pit_col('last_fixed')
    LATEST_AIS = _pit_col('latest_ais')
    SUBCLASS = 'subclass'
    OPEN_PREDICTION_ACCURACY = _pit_col('open_prediction_accuracy')
    OPEN_COUNTRY = _pit_col('open_country')
    OPEN_NARROW_AREA = _pit_col('open_narrow_area')
    OPEN_WIDE_AREA = _pit_col('open_wide_area')

    @staticmethod
    def create_row(vessel: Vessel) -> list:
        return [
            vessel.name,
            vessel.vessel_class,
            vessel.ice_class,
            vessel.year_built,
            vessel.deadweight,
            vessel.length_overall,
            vessel.breadth_extreme,
            vessel.market_deployment,
            vessel.push_type,
            vessel.open_port,
            vessel.open_date,
            vessel.operational_status,
            vessel.commercial_operator,
            vessel.commercial_status,
            vessel.eta,
            vessel.last_fixed,
            vessel.latest_ais,
            vessel.subclass,
            vessel.open_prediction_accuracy,
            vessel.open_country,
            vessel.open_narrow_area,
            vessel.open_wide_area
        ]
