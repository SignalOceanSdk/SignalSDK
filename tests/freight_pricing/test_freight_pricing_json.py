from decimal import Decimal

from signal_ocean.freight_pricing import _freight_pricing_json, Costs, Totals


def test_parses_response_correctly():
    response = [
        {
            "vesselClass": "Suezmax",
            "cargoQuantity": 130000,
            "costs": {
                "freightRate": 5.330548,
                "freightCost": 1439247.960000,
                "canal": 0.0,
                "demurrage": 59000,
            },
            "totals": {
                "totalCost": 1498247.960000,
                "totalCostPerTon": 5.54906651,
            },
        },
        {
            "vesselClass": "Aframax",
            "cargoQuantity": 80000,
            "costs": {
                "freightRate": 8.9608350,
                "freightCost": 1209712.7250000,
                "canal": 20.30,
            },
            "totals": {
                "totalCost": 1249712.7250000,
                "totalCostPerTon": 9.257131,
            },
        },
    ]

    result = _freight_pricing_json.parse(response)

    assert len(result) == 2
    first, second = result

    assert first.vessel_class == "Suezmax"
    assert first.cargo_quantity == Decimal("130000")
    assert first.costs == Costs(
        freight_rate=Decimal("5.330548"),
        freight_cost=Decimal("1439247.960000"),
        canal=Decimal("0.0"),
    )
    assert first.totals == Totals(
        total_cost=Decimal("1498247.960000"),
        total_cost_per_ton=Decimal("5.54906651"),
    )

    assert second.vessel_class == "Aframax"
    assert second.cargo_quantity == Decimal("80000")
    assert second.costs == Costs(
        freight_rate=Decimal("8.9608350"),
        freight_cost=Decimal("1209712.7250000"),
        canal=Decimal("20.30"),
    )
    assert second.totals == Totals(
        total_cost=Decimal("1249712.7250000"),
        total_cost_per_ton=Decimal("9.257131"),
    )
