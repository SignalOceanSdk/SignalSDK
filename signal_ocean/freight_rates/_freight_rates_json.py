from typing import cast, Mapping, Any, List, Tuple, Dict

from .models import FreightPricing, Cost, Port


def parse_freight_pricing(json_list: List[Mapping[str, Any]]) -> \
        Tuple[FreightPricing, ...]:
    pricing_list: List[FreightPricing] = []
    for json in json_list:
        costs = json.get("costs")
        if isinstance(costs, list):
            costs = costs[0]
        empty_ports = [{"name": None, "country": None, "area": None}]
        load_ports = json.get("loadPorts", empty_ports)
        discharge_ports = json.get("dischargePorts", empty_ports)
        pricing = FreightPricing(
            vessel_class=cast(str, json.get("vesselClass")),
            rate=cast(float, json.get("rate")),
            rate_type=cast(str, json.get("rateType")),
            estimated_flat_rate=cast(float, json.get("estimatedFlatRate")),
            costs=Cost(
                canal=costs.get("canal"),
                freight_cost=costs.get("freightCost"),
                other_port_expenses=costs.get("otherPortExpenses"),
            ),
            total_freight_cost=cast(float, json.get("totalFreightCost")),
            total_freight_rate=cast(float, json.get("totalFreightRate")),
            route_type=cast(str, json.get("routeType")),
            load_ports=[Port(name=load_port.get("name"),
                             country=load_port.get("country"),
                             area=load_port.get("area"))
                        for load_port in load_ports],
            discharge_ports=[Port(name=discharge_port.get("name"),
                                  country=discharge_port.get("country"),
                                  area=discharge_port.get("area"))
                             for discharge_port in discharge_ports],
            quantity=cast(float, json.get("quantity")),
            min_flat_augusta_used=cast(bool, json.get("minFlatAugustaUsed")),
            routing_choices=cast(List[str], json.get("routingChoices")),
        )
        pricing_list.append(pricing)
    return tuple(pricing_list)


def parse_ports(json: Mapping[str, Dict[str, str]]) -> Tuple[Port, ...]:
    ports: List[Port] = []
    for port_id, port_details in json.items():
        port = Port(
            id=cast(int, port_id),
            name=port_details["name"],
            country=port_details["country"],
            area=port_details["area"],
        )
        ports.append(port)
    return tuple(ports)
