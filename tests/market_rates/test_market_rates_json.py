import pytest

from signal_ocean.market_rates import MarketRate, Route, \
    _market_rates_json


@pytest.mark.parametrize('rates', [
    ([{"RouteId": "R54", "RateDate": "2020-01-02", "RateValue": 21.2219,
       "Unit": "PMT", "VesselClassId": 77},
      {"RouteId": "R55", "RateDate": "2020-01-02", "RateValue": 19.65788,
       "Unit": "PMT", "VesselClassId": 77}
      ])
])
def test_parse_market_rates(rates):
    mr_object = _market_rates_json.parse_market_rates(rates)

    assert type(mr_object) is tuple
    for mr, rate in zip(mr_object, rates):
        assert isinstance(mr, MarketRate)
        assert mr.route_id == rate["RouteId"]
        assert mr.rate_date == rate["RateDate"]
        assert mr.rate_value == rate["RateValue"]
        assert mr.unit == rate["Unit"]
        assert mr.vessel_class_id == rate["VesselClassId"]


@pytest.mark.parametrize('routes', [
    ([{"route_id": "R1", "description": "Afra - Med", "unit": "WS",
       "vessel_class_id": 86, "is_clean": False},
      {"route_id": "R10", "description": "Afra - Indo_OZ", "unit": "WS",
       "vessel_class_id": 86, "is_clean": False}
      ])
])
def test_parse_routes(routes):
    r_object = _market_rates_json.parse_routes(routes)

    assert type(r_object) is tuple
    for r, route in zip(r_object, routes):
        assert isinstance(r, Route)
        assert r.id == route["route_id"]
        assert r.description == route["description"]
        assert r.unit == route["unit"]
        assert r.vessel_class_id == route["vessel_class_id"]
        assert r.is_clean == route["is_clean"]
