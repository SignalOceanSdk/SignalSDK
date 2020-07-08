from datetime import datetime, timezone
from typing import List, Union

from dateutil import parser

from .historical_tonnage_list import HistoricalTonnageList
from .tonnage_list import TonnageList
from .vessel import Vessel
from .open_area import OpenArea


def parse(json) -> HistoricalTonnageList:
    static_vessel_data = json.get('staticVesselData', [])
    tonnage_lists = json.get('tonnageLists', [])

    return HistoricalTonnageList(
        (_to_tonnage_list(tl, static_vessel_data) for tl in tonnage_lists)
    )


def _parse_datetime(value: str) -> Union[datetime, None]:
    if not value:
        return None
    try:
        result = parser.isoparse(value)
    except (TypeError, ValueError):
        return None

    return result.replace(tzinfo=timezone.utc)


def _to_vessel(pit_vessel_data: dict, static_vessel_data: List[dict]) -> Vessel:
    imo = pit_vessel_data['imo']

    data_for_imo = {}
    for svd in static_vessel_data:
        if svd['imo'] == imo:
            data_for_imo = svd
            break

    return Vessel(
        imo,
        data_for_imo.get('vesselName'),
        data_for_imo.get('vesselClass'),
        data_for_imo.get('iceClass'),
        data_for_imo.get('yearBuilt'),
        data_for_imo.get('deadWeight'),
        data_for_imo.get('lengthOverall'),
        data_for_imo.get('breadthExtreme'),
        pit_vessel_data.get('marketDeployment'),
        pit_vessel_data.get('pushType'),
        pit_vessel_data.get('openPort'),
        _parse_datetime(pit_vessel_data.get('openDate')),
        pit_vessel_data.get('operationalStatus'),
        pit_vessel_data.get('commercialOperator'),
        pit_vessel_data.get('commercialStatus'),
        _parse_datetime(pit_vessel_data.get('eta')),
        pit_vessel_data.get('lastFixed'),
        _parse_datetime(pit_vessel_data.get('latestAis')),
        data_for_imo.get('subclass'),
        data_for_imo.get('willingToSwitchSubclass'),
        pit_vessel_data.get('openPredictionAccuracy'),
        tuple(
            OpenArea(a.get('name'), a.get('locationTaxonomy'))
            for a in pit_vessel_data.get('openAreas', [])
        )
    )


def _to_tonnage_list(
        tonnage_list_json: dict,
        static_vessel_data: List[dict]) -> TonnageList:
    date = _parse_datetime(tonnage_list_json['date'])
    vessels = tuple(
        _to_vessel(pit_vessel_data, static_vessel_data) for pit_vessel_data in
        tonnage_list_json.get('pointInTimeVesselData', [])
    )

    return TonnageList(date, vessels)
