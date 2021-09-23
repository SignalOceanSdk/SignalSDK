from typing import Any, List, Mapping

from .models import TonnageList
from ..historical_tonnage_list._historical_tonnage_list_json import to_vessel


def parse_tonnage_list(json: Mapping[str, Any]) -> TonnageList:
    tonnage_list: List[Mapping[str, Any]] = json.get("tonnageList", [])
    static_vessel_data: List[Mapping[str, Any]] = json.get(
        "staticVesselData", []
    )

    return TonnageList(
        (to_vessel(pit_data, static_vessel_data) for pit_data in tonnage_list)
    )
