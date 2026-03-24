from typing import cast, Mapping, Any, List, Tuple

from .models import PortExpenses, Port


def parse_port_expenses(json: Mapping[str, Any]) -> PortExpenses:
    return PortExpenses(
        port_id=cast(int, json.get("PortId")),
        towage=cast(int, json.get("Towage")),
        port_dues=cast(int, json.get("PortDues")),
        pilotage=cast(int, json.get("Pilotage")),
        agency_fees=cast(int, json.get("AgencyFees")),
        other=cast(int, json.get("Other")),
        suez_dues=cast(int, json.get("SuezDues")),
        total_cost=cast(int, json.get("TotalCost")),
        miscellaneous_dues=cast(int, json.get("MiscellaneousDues")),
        is_estimated=cast(bool, json.get("IsEstimated")),
        canal_dues=cast(int, json.get("CanalDues")),
        berth_dues=cast(int, json.get("BerthDues")),
        lighthouse_dues=cast(int, json.get("LighthouseDues")),
        mooring_unmooring=cast(int, json.get("MooringUnmooring")),
        quay_dues=cast(int, json.get("QuayDues")),
        anchorage_dues=cast(int, json.get("AnchorageDues")),
    )


def parse_ports(json: Mapping[str, Any]) -> Tuple[Port, ...]:
    ports: List[Port] = []
    json_ports = json.get("Ports")
    if json_ports is not None and isinstance(json_ports, list):
        for port_json in json_ports:
            port = Port(
                id=cast(int, port_json.get("PortId")),
                name=cast(str, port_json.get("PortName")),
            )
            ports.append(port)
    return tuple(ports)
