from typing import cast, Mapping, Any, List

from .models import PortExpenses, CanalExpenses


def parse_port_expenses(json: Mapping[str, Any]) -> PortExpenses:
    return PortExpenses(
        cast(int, json.get("PortId")),
        cast(int, json.get("PortCanal")),
        cast(int, json.get("Towage")),
        cast(int, json.get("Berth")),
        cast(int, json.get("PortDues")),
        cast(int, json.get("Lighthouse")),
        cast(int, json.get("Mooring")),
        cast(int, json.get("Pilotage")),
        cast(int, json.get("Quay")),
        cast(int, json.get("Anchorage")),
        cast(int, json.get("AgencyFees")),
        cast(int, json.get("Other")),
        cast(int, json.get("SuezDues")),
        cast(int, json.get("TotalCost")),
        cast(int, json.get("MiscellaneousDues")),
        cast(bool, json.get("IsEstimated")),
        cast(int, json.get("CanalDues")),
        cast(int, json.get("BerthDues")),
        cast(int, json.get("LighthouseDues")),
        cast(int, json.get("MooringUnmooring")),
        cast(int, json.get("QuayDues")),
        cast(int, json.get("AnchorageDues")),
        cast(List[int], json.get("PortAgents")),
    )


def parse_canal_expenses(json: Mapping[str, Any]) -> CanalExpenses:
    return CanalExpenses(
        cast(int, json.get("TotalCost"))
    )