import pytest

from signal_ocean.port_expenses import PortExpenses, Port
from signal_ocean.port_expenses import _port_expenses_json


@pytest.mark.parametrize('port_id, port_canal, towage, port_dues, pilotage, '
    'agency_fees, other, suez_dues, total_cost, miscellaneous_dues, '
    'is_estimated, canal_dues, berth_dues, lighthouse_dues, mooring_unmooring, '
    'quay_dues, anchorage_dues, port_agents', [
    (3153, 0, 0, 40196, 0, 1500, 2277, 0, 44568, 0, False, 0, 0, 0, 0, 0, 0, [])
])
def test_parse_port_expenses(port_id, port_canal, towage, port_dues, pilotage,
    agency_fees, other, suez_dues, total_cost, miscellaneous_dues, is_estimated,
    canal_dues, berth_dues, lighthouse_dues, mooring_unmooring, quay_dues,
    anchorage_dues, port_agents):
    port_expenses_json = {
        "PortId": port_id,
        "PortCanal": port_canal,
        "Towage": towage,
        "PortDues": port_dues,
        "Pilotage": pilotage,
        "AgencyFees": agency_fees,
        "Other": other,
        "SuezDues": suez_dues,
        "TotalCost": total_cost,
        "MiscellaneousDues": miscellaneous_dues,
        "IsEstimated": is_estimated,
        "CanalDues": canal_dues,
        "BerthDues": berth_dues,
        "LighthouseDues": lighthouse_dues,
        "MooringUnmooring": mooring_unmooring,
        "QuayDues": quay_dues,
        "AnchorageDues": anchorage_dues,
        "PortAgents": port_agents
    }

    pe_object = _port_expenses_json.parse_port_expenses(port_expenses_json)

    assert type(pe_object) is PortExpenses
    assert pe_object.port_id == port_id
    assert pe_object.port_canal == port_canal
    assert pe_object.towage == towage
    assert pe_object.port_dues == port_dues
    assert pe_object.pilotage == pilotage
    assert pe_object.agency_fees == agency_fees
    assert pe_object.other == other
    assert pe_object.suez_dues == suez_dues
    assert pe_object.total_cost == total_cost
    assert pe_object.miscellaneous_dues == miscellaneous_dues
    assert pe_object.is_estimated == is_estimated
    assert pe_object.canal_dues == canal_dues
    assert pe_object.berth_dues == berth_dues
    assert pe_object.lighthouse_dues == lighthouse_dues
    assert pe_object.mooring_unmooring == mooring_unmooring
    assert pe_object.quay_dues == quay_dues
    assert pe_object.anchorage_dues == anchorage_dues
    assert pe_object.port_agents == port_agents


@pytest.mark.parametrize('ports', [
    ([{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"},
      {"id": 3, "name": "test3"}])
])
def test_parse_ports(ports):
    ports_json = {
        "Ports": [{"PortId": p["id"], "PortName": p["name"]} for p in ports]
    }

    ports_object = _port_expenses_json.parse_ports(ports_json)

    for i, port in enumerate(ports_object):
        assert type(port) is Port
        assert port.id == ports[i]["id"]
        assert port.name == ports[i]["name"]
