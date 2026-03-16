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
        open_port_id=cast(int, pit_vessel_data.get("openPortId")),
        open_port=cast(str, pit_vessel_data.get("openPort")),
        open_date=parse_datetime(pit_vessel_data.get("openDate")),
        operational_status=cast(str, pit_vessel_data.get("operationalStatus")),
        commercial_operator_id=cast(int, pit_vessel_data.get("commercialOperatorId")),
        commercial_operator=cast(str, pit_vessel_data.get("commercialOperator")),
        commercial_status=cast(str, pit_vessel_data.get("commercialStatus")),
        eta=parse_datetime(pit_vessel_data.get("eta")),
        latest_ais=parse_datetime(pit_vessel_data.get("latestAis")),
        subclass=cast(str, data_for_imo.get("subclass")),
        willing_to_switch_subclass=cast(bool, data_for_imo.get("willingToSwitchSubclass")),
        open_prediction_accuracy=cast(str, pit_vessel_data.get("openPredictionAccuracy")),
        open_areas=tuple(
            Area(
                id=a.get("id"),
                name=a.get("name"),
                location_taxonomy=a.get("locationTaxonomy"),
                taxonomy_id=a.get("taxonomyId"),
            )
            for a in pit_vessel_data.get("openAreas", [])
        ),
        availability_port_type=cast(str, pit_vessel_data.get("availabilityPortType")),
        availability_date_type=cast(str, pit_vessel_data.get("availabilityDateType")),
        fixture_type=cast(str, pit_vessel_data.get("fixtureType")),
        current_vessel_sub_type_id=cast(int, pit_vessel_data.get("currentVesselSubTypeId")),
        current_vessel_sub_type=cast(str, pit_vessel_data.get("currentVesselSubType")),
        willing_to_switch_current_vessel_sub_type=cast(bool, pit_vessel_data.get("willingToSwitchCurrentVesselSubType")),
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
