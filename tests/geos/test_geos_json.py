from decimal import Decimal

from signal_ocean.geos import _geo_json, Country, Port, Area


def test_parses_countries_correctly():
    country_json = {
        "country_id": 1,
        "country_name": "country1",
        "location_taxonomy_id": 0,
        "location_taxonomy_name": "ccn1",
    }

    country = _geo_json.parse_country(country_json)

    assert type(country) is Country
    assert country.country_id == 1
    assert country.country_name == "country1"
    assert country.location_taxonomy_id == 0
    assert country.location_taxonomy_name == "ccn1"


def test_parses_ports_correctly():
    port_json = {
        "id": 1,
        "countryId": 2,
        "areaId": 3,
        "name": "port",
        "latitude": 45.6789,
        "longitude": 56.789
    }

    port = _geo_json.parse_port(port_json)

    assert type(port) is Port
    assert port.id == 1
    assert port.country_id == 2
    assert port.area_id == 3
    assert port.name == "port"
    assert port.latitude == Decimal("45.6789")
    assert port.longitude == Decimal("56.789")


def test_parses_areas_correctly():
    area_json = {"id": 1, "name": "area", "areaTypeId": 2, "parentAreaId": 3}

    area = _geo_json.parse_area(area_json)

    assert type(area) is Area
    assert area.id == 1
    assert area.name == "area"
    assert area.area_type_id == 2
    assert area.parent_area_id == 3
