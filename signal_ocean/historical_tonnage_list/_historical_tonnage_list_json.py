from datetime import datetime
from typing import Iterable, cast, Mapping, Any, Tuple

from .tonnage_list import TonnageList
from .vessel import Vessel
from .area import Area
from .._internals import parse_datetime


def parse_tonnage_lists(json: Mapping[str, Any]) -> Tuple[TonnageList, ...]:
    static_vessel_data = json.get("staticVesselData", [])
    tonnage_lists = json.get("tonnageLists", [])

    return tuple(
        to_tonnage_list(tl, static_vessel_data) for tl in tonnage_lists
    )


def to_vessel(
    pit_vessel_data: Mapping[str, Any],
    static_vessel_data: Iterable[Mapping[str, Any]],
) -> Vessel:
    imo = pit_vessel_data["imo"]
    data_for_imo: Mapping[str, Any] = next(
        (svd for svd in static_vessel_data if svd["imo"] == imo), {}
    )

    return Vessel(
        imo,
        cast(str, data_for_imo.get("vesselName")),
        cast(str, data_for_imo.get("vesselClass")),
        data_for_imo.get("iceClass"),
        cast(int, data_for_imo.get("yearBuilt")),
        cast(int, data_for_imo.get("deadWeight")),
        cast(float, data_for_imo.get("lengthOverall")),
        cast(int, data_for_imo.get("breadthExtreme")),
        cast(str, pit_vessel_data.get("marketDeployment")),
        cast(str, pit_vessel_data.get("pushType")),
        cast(str, pit_vessel_data.get("openPort")),
        parse_datetime(pit_vessel_data.get("openDate")),
        cast(str, pit_vessel_data.get("operationalStatus")),
        cast(str, pit_vessel_data.get("commercialOperator")),
        cast(str, pit_vessel_data.get("commercialStatus")),
        parse_datetime(pit_vessel_data.get("eta")),
        parse_datetime(pit_vessel_data.get("latestAis")),
        cast(str, data_for_imo.get("subclass")),
        cast(bool, data_for_imo.get("willingToSwitchSubclass")),
        cast(str, pit_vessel_data.get("openPredictionAccuracy")),
        tuple(
            Area(a.get("name"), a.get("locationTaxonomy"))
            for a in pit_vessel_data.get("openAreas", [])
        ),
        cast(str, pit_vessel_data.get("availabilityPortType")),
        cast(str, pit_vessel_data.get("availabilityDateType")),
    )


def to_tonnage_list(
    tonnage_list_json: Mapping[str, Any],
    static_vessel_data: Iterable[Mapping[str, Any]],
) -> TonnageList:
    date = cast(datetime, parse_datetime(tonnage_list_json["date"]))
    vessels = tuple(
        to_vessel(pit_vessel_data, static_vessel_data)
        for pit_vessel_data in tonnage_list_json.get(
            "pointInTimeVesselData", []
        )
    )

    return TonnageList(date, vessels)
