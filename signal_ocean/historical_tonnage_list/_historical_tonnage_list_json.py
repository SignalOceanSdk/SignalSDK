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
        imo=imo,
        name=cast(str, data_for_imo.get("vesselName")),
        vessel_class=cast(str, data_for_imo.get("vesselClass")),
        ice_class=data_for_imo.get("iceClass"),
        year_built=cast(int, data_for_imo.get("yearBuilt")),
        deadweight=cast(int, data_for_imo.get("deadWeight")),
        length_overall=cast(float, data_for_imo.get("lengthOverall")),
        breadth_extreme=cast(int, data_for_imo.get("breadthExtreme")),
        market_deployment=cast(str, pit_vessel_data.get("marketDeployment")),
        push_type=cast(str, pit_vessel_data.get("pushType")),
        open_port=cast(str, pit_vessel_data.get("openPort")),
        open_date=parse_datetime(pit_vessel_data.get("openDate")),
        operational_status=cast(str, pit_vessel_data.get("operationalStatus")),
        commercial_operator=cast(str, pit_vessel_data.get("commercialOperator")),
        commercial_status=cast(str, pit_vessel_data.get("commercialStatus")),
        eta=parse_datetime(pit_vessel_data.get("eta")),
        latest_ais=parse_datetime(pit_vessel_data.get("latestAis")),
        subclass=cast(str, data_for_imo.get("subclass")),
        willing_to_switch_subclass=cast(bool, data_for_imo.get("willingToSwitchSubclass")),
        open_prediction_accuracy=cast(str, pit_vessel_data.get("openPredictionAccuracy")),
        open_areas=tuple(
            Area(name=a.get("name"), location_taxonomy=a.get("locationTaxonomy"))
            for a in pit_vessel_data.get("openAreas", [])
        ),
        availability_port_type=cast(str, pit_vessel_data.get("availabilityPortType")),
        availability_date_type=cast(str, pit_vessel_data.get("availabilityDateType")),
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
