# noqa: D100

from decimal import Decimal

from signal_ocean.util.pydantic_base import SignalBaseModel


class Totals(SignalBaseModel):
    """Total costs of moving freight.

    Attributes:
        total_cost: Total transportation cost in $. A sum of freight, canal,
            and demurrage costs.
        total_cost_per_ton: Total cost per ton in $.
    """

    total_cost: Decimal
    total_cost_per_ton: Decimal


class Costs(SignalBaseModel):
    """Individual costs of moving freight.

    Attributes:
        freight_rate: Cost of freight in $ per ton.
        freight_cost: Cost of transporting the given quentity between the
            selected load and discharge port in $.
        canal: Cost of passing through canals in $.
    """

    freight_rate: Decimal
    freight_cost: Decimal
    canal: Decimal


class FreightPricing(SignalBaseModel):
    """Freight pricing for a specific vessel class.

    Attributes:
        vessel_class: The vessel class the pricing applies to.
        cargo_quantity: Cargo quantity for the selected load and discharge
            ports.
        costs: Individual costs of moving freight.
        totals: Total costs of moving freight.
    """

    vessel_class: str
    cargo_quantity: Decimal
    costs: Costs
    totals: Totals
