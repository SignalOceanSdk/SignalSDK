from decimal import Decimal

from signal_ocean.freight_pricing import _freight_pricing_json


def test_parses_response_correctly():
    response = [
        {
            'vesselClass': 'Suezmax',
            'cargoQuantity': 130000,
            'rate': 24.390015,
            'totalFreight': 3170701.950000
        },
        {
            'vesselClass': 'Aframax',
            'cargoQuantity': 80000,
            'rate': 34.0176525,
            'totalFreight': 2721412.2000000
        }
    ]

    result = _freight_pricing_json.parse(response)

    assert len(result) == 2
    first, second = result

    assert first.vessel_class == 'Suezmax'
    assert first.cargo_quantity == Decimal('130000')
    assert first.rate == Decimal('24.390015')
    assert first.total_freight == Decimal('3170701.950000')

    assert second.vessel_class == 'Aframax'
    assert second.cargo_quantity == Decimal('80000')
    assert second.rate == Decimal('34.0176525')
    assert second.total_freight == Decimal('2721412.2000000')


def test_handles_missing_properties_on_freight_pricing_items():
    item_json = {
        'vesselClass': None,
        'cargoQuantity': None,
        'rate': None,
        'totalFreight': None
    }

    item = _freight_pricing_json.parse_freight_pricing_item(item_json)

    assert item.vessel_class is None
    assert item.cargo_quantity is None
    assert item.rate is None
    assert item.total_freight is None
