from signal_ocean.historical_tonnage_list import Column
from .create_vessel import create_vessel


def test_can_list_all_column_names():
    columns = list(Column)

    assert columns == [
        'name',
        'vessel_class',
        'ice_class',
        'year_built',
        'deadweight',
        'length_overall',
        'breadth_extreme',
        'market_deployment_point_in_time',
        'push_type_point_in_time',
        'open_port_point_in_time',
        'open_date_point_in_time',
        'operational_status_point_in_time',
        'commercial_operator_point_in_time',
        'commercial_status_point_in_time',
        'eta_point_in_time',
        'last_fixed_point_in_time',
        'latest_ais_point_in_time',
        'subclass',
        'open_prediction_accuracy_point_in_time',
        'open_country_point_in_time',
        'open_narrow_area_point_in_time',
        'open_wide_area_point_in_time',
        'availability_port_type_point_in_time',
        'availability_date_type_point_in_time',
        'liquid_capacity',
        'fixture_type_point_in_time'
    ]


def test_places_vessel_data_in_correct_columns():
    vessel = create_vessel()

    row = Column._create_row(vessel)

    assert row == [
        vessel.name,
        vessel.vessel_class,
        vessel.ice_class,
        vessel.year_built,
        vessel.deadweight,
        vessel.length_overall,
        vessel.breadth_extreme,
        vessel.market_deployment,
        vessel.push_type,
        vessel.open_port,
        vessel.open_date,
        vessel.operational_status,
        vessel.commercial_operator,
        vessel.commercial_status,
        vessel.eta,
        vessel.last_fixed,
        vessel.latest_ais,
        vessel.subclass,
        vessel.open_prediction_accuracy,
        vessel.open_country,
        vessel.open_narrow_area,
        vessel.open_wide_area,
        vessel.availability_port_type,
        vessel.availability_date_type,
        vessel.liquid_capacity,
        vessel.fixture_type
    ]


def test_has_overrides_for_column_data_types():
    assert Column._get_data_types() == {
        'vessel_class': 'category',
        'ice_class': 'category',
        'market_deployment_point_in_time': 'category',
        'push_type_point_in_time': 'category',
        'open_port_point_in_time': 'category',
        'operational_status_point_in_time': 'category',
        'commercial_operator_point_in_time': 'category',
        'commercial_status_point_in_time': 'category',
        'subclass': 'category',
        'open_prediction_accuracy_point_in_time': 'category',
        'open_country_point_in_time': 'category',
        'open_narrow_area_point_in_time': 'category',
        'open_wide_area_point_in_time': 'category',
        'availability_port_type_point_in_time': 'category',
        'availability_date_type_point_in_time': 'category',
        'fixture_type_point_in_time': 'category'
    }
