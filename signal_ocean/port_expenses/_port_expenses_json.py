from typing import cast, Mapping, Any, List, Tuple

from .models import PortExpenses, Port


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


def parse_ports(json: Mapping[str, Any]) -> Tuple[Port, ...]:
    ports: List[Port] = []
    json_ports = json.get("Ports")
    if json_ports is not None and isinstance(json_ports, list):
        for port_json in json_ports:
            port = Port(
                cast(int, port_json.get("PortId")),
                cast(str, port_json.get("PortName")),
            )
            ports.append(port)
    return tuple(ports)
