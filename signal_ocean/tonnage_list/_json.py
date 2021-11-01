from datetime import datetime
from typing import Any, Iterable, List, Mapping, cast

from .models import Area, HistoricalTonnageList, TonnageList, Vessel
from .._internals import parse_datetime


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
    pit_data: List[Mapping[str, Any]],
    static_vessel_data: List[Mapping[str, Any]],
    date: datetime,
) -> TonnageList:
    return TonnageList(
        (to_vessel(pd, static_vessel_data) for pd in pit_data), date,
    )


def parse_tonnage_list_response(json: Mapping[str, Any]) -> TonnageList:
    tonnage_list: List[Mapping[str, Any]] = json.get("tonnageList", [])
    static_vessel_data: List[Mapping[str, Any]] = json.get(
        "staticVesselData", []
    )

    return to_tonnage_list(tonnage_list, static_vessel_data, datetime.utcnow())


def parse_historical_tonnage_list_response(
    json: Mapping[str, Any]
) -> HistoricalTonnageList:
    static_vessel_data = json.get("staticVesselData", [])
    tonnage_lists = json.get("tonnageLists", [])

    return HistoricalTonnageList(
        to_tonnage_list(
            tl["pointInTimeVesselData"],
            static_vessel_data,
            cast(datetime, parse_datetime(tl["date"])),
        )
        for tl in tonnage_lists
    )
