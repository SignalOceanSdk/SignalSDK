# noqa: D100

from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class Cost:
    """The freight costs breakdown.

    Attributes:
        canal: Canal costs.
        freight_cost: Freight cost.
        other_port_expenses: Other port expenses.
    """

    canal: float
    freight_cost: float
    other_port_expenses: float


@dataclass(frozen=True)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: ID of the port.
        name: Name of the port.
        country: Country of the port.
        area: Area of the port.
    """

    name: str
    id: Optional[int] = None
    country: Optional[str] = None
    area: Optional[str] = None


@dataclass(frozen=True)
class FreightPricing:
    """The freight pricing given a load and discharge port.

    Attributes:
        vessel_class: The vessel class.
        rate: Value of the rate.
        rate_type: Type of the rate.
        estimated_flat_rate: Estimated flat rate.
        costs: Costs breakdown.
        total_freight_cost: Total freight cost.
        total_freight_rate: Total freight rate.
        route_type: Route type.
        load_ports: Load ports.
        discharge_ports: Discharge ports.
        quantity: Quantity.
        min_flat_augusta_used: True if minimum flat Augusta was used.
        routing_choices: Routing choices (e.g. Suez, Panama etc).
    """

    vessel_class: str
    rate: float
    rate_type: str
    estimated_flat_rate: float
    costs: Cost
    total_freight_cost: float
    total_freight_rate: float
    route_type: str
    load_ports: List[Port]
    discharge_ports: List[Port]
    quantity: float
    min_flat_augusta_used: bool
    routing_choices: Optional[List[str]]
