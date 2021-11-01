import pytest

from signal_ocean.freight_rates import FreightPricing, _freight_rates_json


@pytest.mark.parametrize('pricing', [
    ([
        {
            "vesselClass": "VLCC",
            "rate": 40,
            "rateType": "WorldScale",
            "estimatedFlatRate": 2.6777,
            "costs": [
                {
                    "canal": 0,
                    "freightCost": 289191.6
                }
            ],
            "totalFreightCost": 289191.6,
            "totalFreightRate": 1.07108,
            "routeType": "Unknown",
            "routingChoices": [],
            "loadPort": {
                "name": "Fujairah",
                "country": "United Arab Emirates",
                "area": "Arabian Gulf"
            },
            "dischargePort": {
                "name": "Jebel Ali",
                "country": "United Arab Emirates",
                "area": "Arabian Gulf"
            },
            "quantity": 270000,
            "minFlatAugustaUsed": False
        },
        {
            "vesselClass": "Aframax",
            "rate": 435000,
            "rateType": "LumpSum",
            "estimatedFlatRate": 2.6777,
            "costs": [
                {
                "canal": 0,
                "freightCost": 435000
                }
            ],
            "totalFreightCost": 435000,
            "totalFreightRate": 5.4375,
            "routeType": "Unknown",
            "routingChoices": [],
            "loadPort": {
                "name": "Fujairah",
                "country": "United Arab Emirates",
                "area": "Arabian Gulf"
            },
            "dischargePort": {
                "name": "Jebel Ali",
                "country": "United Arab Emirates",
                "area": "Arabian Gulf"
            },
            "quantity": 80000,
            "minFlatAugustaUsed": False
        }
    ])
])
def test_parse_freight_pricing(pricing):
    fp_object = _freight_rates_json.parse_freight_pricing(pricing)
    assert type(fp_object) is tuple
    for fp, data in zip(fp_object, pricing):
        assert isinstance(fp, FreightPricing)
        assert fp.vessel_class == data["vesselClass"]
        assert fp.rate == data["rate"]
        assert fp.rate_type == data["rateType"]
        assert fp.estimated_flat_rate == data["estimatedFlatRate"]
        assert fp.costs.canal == data["costs"][0]["canal"]
        assert fp.costs.freight_cost == data["costs"][0]["freightCost"]
        assert fp.total_freight_cost == data["totalFreightCost"]
        assert fp.total_freight_rate == data["totalFreightRate"]
        assert fp.route_type == data["routeType"]
        assert fp.routing_choices == data["routingChoices"]
        assert fp.load_port.name == data["loadPort"]["name"]
        assert fp.load_port.country == data["loadPort"]["country"]
        assert fp.load_port.area == data["loadPort"]["area"]
        assert fp.discharge_port.name == data["dischargePort"]["name"]
        assert fp.discharge_port.country == data["dischargePort"]["country"]
        assert fp.discharge_port.area == data["dischargePort"]["area"]
        assert fp.quantity == data["quantity"]
        assert fp.min_flat_augusta_used == data["minFlatAugustaUsed"]
