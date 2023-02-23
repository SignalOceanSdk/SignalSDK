from datetime import date

from unittest.mock import MagicMock

import pytest

from signal_ocean.freight_rates import FreightRatesAPI, FreightPricing
from signal_ocean.freight_rates.enums import VesselClass


@pytest.mark.parametrize('load_ports, discharge_ports, vessel_classes, '
                         'is_clean, date, ',
                         [
                             ([3153, 3211], [3157, 3158], ["VLCC", "Aframax"],
                              0, date.today())
                         ])
def test_get_freight_pricing(load_ports, discharge_ports, vessel_classes,
                             is_clean, date):
    connection = MagicMock()
    api = FreightRatesAPI(connection)

    fp_object = api.get_freight_pricing(load_ports, discharge_ports,
                                        vessel_classes, is_clean, date)

    assert isinstance(fp_object, tuple)
    assert all([isinstance(fp, FreightPricing) for fp in fp_object])

    query_dict = {
        "LoadPorts": '&LoadPorts='.join([str(lp) for lp in load_ports]),
        "DischargePorts": '&DischargePorts='.join([str(dp) for dp in
                                                       discharge_ports]),
        "IsClean": '{}'.format(is_clean),
        "Date": date.isoformat()
    }

    vessel_classes_param = '&VesselClasses='.join(vessel_classes)
    query_dict['VesselClasses'] = vessel_classes_param

    connection._make_get_request.assert_called_with(
        "freight/api/Freight/v3/pricing",
        query_dict
    )


def test_get_vessel_classes():
    connection = MagicMock()
    api = FreightRatesAPI(connection)

    vessel_classes = api.get_vessel_classes()

    assert vessel_classes == tuple(vessel_class.name for
                                   vessel_class in VesselClass)
