from datetime import date

from unittest.mock import MagicMock

import pytest

from signal_ocean.freight_rates import FreightRatesAPI, FreightPricing
from signal_ocean.freight_rates.enums import VesselClass


@pytest.mark.parametrize('load_port_id, discharge_port_id, vessel_classes, '
                         'is_clean, date, ',
                         [
                             (3153, 3157, ["VLCC", "Aframax"], 0,
                              date.today())
                         ])
def test_get_freight_pricing(load_port_id, discharge_port_id, vessel_classes,
                             is_clean, date):
    connection = MagicMock()
    api = FreightRatesAPI(connection)

    fp_object = api.get_freight_pricing(load_port_id, discharge_port_id,
                                        vessel_classes, is_clean, date)

    assert isinstance(fp_object, tuple)
    assert all([isinstance(fp, FreightPricing) for fp in fp_object])

    query_dict = {
        "LoadPortId": '{}'.format(load_port_id),
        "DischargePortId": '{}'.format(discharge_port_id),
        "IsClean": '{}'.format(is_clean),
        "Date": date.isoformat()
    }

    vessel_classes_param = '&VesselClasses='.join(vessel_classes)
    query_dict['VesselClasses'] = vessel_classes_param

    connection._make_get_request.assert_called_with(
        "freight/api/Freight/v2/pricing",
        query_dict
    )


def test_get_vessel_classes():
    connection = MagicMock()
    api = FreightRatesAPI(connection)

    vessel_classes = api.get_vessel_classes()

    assert vessel_classes == tuple(vessel_class.name for
                                   vessel_class in VesselClass)
