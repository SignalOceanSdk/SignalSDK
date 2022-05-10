from typing import cast, Mapping, Any, List, Tuple, Dict

from .models import FreightPricing, Cost, Port


def parse_freight_pricing(json_list: List[Mapping[str, Any]]) -> \
        Tuple[FreightPricing, ...]:
    pricing_list: List[FreightPricing] = []
    for json in json_list:
        costs = json.get("costs")
        if isinstance(costs, list):
            costs = costs[0]
        empty_port = {"name": None, "country": None, "area": None}
        load_port = json.get("loadPort", empty_port)
        discharge_port = json.get("dischargePort", empty_port)
        pricing = FreightPricing(
            cast(str, json.get("vesselClass")),
            cast(float, json.get("rate")),
            cast(str, json.get("rateType")),
            cast(float, json.get("estimatedFlatRate")),
            Cost(costs.get("canal"), costs.get("freightCost"),
                 costs.get("otherPortExpenses")),
            cast(float, json.get("totalFreightCost")),
            cast(float, json.get("totalFreightRate")),
            cast(str, json.get("routeType")),
            Port(name=load_port.get("name"),
                 country=load_port.get("country"),
                 area=load_port.get("area")),
            Port(name=discharge_port.get("name"),
                 country=discharge_port.get("country"),
                 area=discharge_port.get("area")),
            cast(float, json.get("quantity")),
            cast(bool, json.get("minFlatAugustaUsed")),
            cast(List[str], json.get("routingChoices")),
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
