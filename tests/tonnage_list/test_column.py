from itertools import takewhile, dropwhile

from signal_ocean.tonnage_list import Column
from .builders import create_vessel


def test_can_list_all_column_names() -> None:
    columns = list(Column)

    assert columns == [
        "name",
        "vessel_class",
        "ice_class",
        "year_built",
        "deadweight",
        "length_overall",
        "breadth_extreme",
        "subclass",
        "market_deployment_point_in_time",
        "push_type_point_in_time",
        "open_port_id_point_in_time",
        "open_port_point_in_time",
        "open_date_point_in_time",
        "operational_status_point_in_time",
        "commercial_operator_id_point_in_time",
        "commercial_operator_point_in_time",
        "commercial_status_point_in_time",
        "eta_point_in_time",
        "latest_ais_point_in_time",
        "open_prediction_accuracy_point_in_time",
        "open_country_point_in_time",
        "open_narrow_area_point_in_time",
        "open_wide_area_point_in_time",
        "availability_port_type_point_in_time",
        "availability_date_type_point_in_time",
        "fixture_type_point_in_time",
        "current_vessel_sub_type_id_point_in_time",
        "current_vessel_sub_type_point_in_time",
        "willing_to_switch_current_vessel_sub_type_point_in_time",
    ]


def test_places_vessel_data_in_correct_columns() -> None:
    vessel = create_vessel()

    row = Column._create_row(
        vessel.name,
        vessel.vessel_class,
        vessel.ice_class,
        vessel.year_built,
        vessel.deadweight,
        vessel.length_overall,
        vessel.breadth_extreme,
        vessel.subclass,
        vessel.market_deployment,
        vessel.push_type,
        vessel.open_port_id,
        vessel.open_port,
        vessel.open_date,
        vessel.operational_status,
        vessel.commercial_operator_id,
        vessel.commercial_operator,
        vessel.commercial_status,
        vessel.eta,
        vessel.latest_ais,
        vessel.open_prediction_accuracy,
        vessel.open_country,
        vessel.open_narrow_area,
        vessel.open_wide_area,
        vessel.availability_port_type,
        vessel.availability_date_type,
        vessel.fixture_type,
        vessel.current_vessel_sub_type_id,
        vessel.current_vessel_sub_type,
        vessel.willing_to_switch_current_vessel_sub_type,
    )

    assert row == (
        vessel.name,
        vessel.vessel_class,
        vessel.ice_class,
        vessel.year_built,
        vessel.deadweight,
        vessel.length_overall,
        vessel.breadth_extreme,
        vessel.subclass,
        vessel.market_deployment,
        vessel.push_type,
        vessel.open_port_id,
        vessel.open_port,
        vessel.open_date,
        vessel.operational_status,
        vessel.commercial_operator_id,
        vessel.commercial_operator,
        vessel.commercial_status,
        vessel.eta,
        vessel.latest_ais,
        vessel.open_prediction_accuracy,
        vessel.open_country,
        vessel.open_narrow_area,
        vessel.open_wide_area,
        vessel.availability_port_type,
        vessel.availability_date_type,
        vessel.fixture_type,
        vessel.current_vessel_sub_type_id,
        vessel.current_vessel_sub_type,
        vessel.willing_to_switch_current_vessel_sub_type,
    )


def test_has_overrides_for_column_data_types() -> None:
    assert Column._get_data_types() == {
        "vessel_class": "category",
        "ice_class": "category",
        "market_deployment_point_in_time": "category",
        "push_type_point_in_time": "category",
        "open_port_id_point_in_time": "category",
        "open_port_point_in_time": "category",
        "operational_status_point_in_time": "category",
        "commercial_operator_id_point_in_time": "category",
        "commercial_operator_point_in_time": "category",
        "commercial_status_point_in_time": "category",
        "subclass": "category",
        "open_prediction_accuracy_point_in_time": "category",
        "open_country_point_in_time": "category",
        "open_narrow_area_point_in_time": "category",
        "open_wide_area_point_in_time": "category",
        "availability_port_type_point_in_time": "category",
        "availability_date_type_point_in_time": "category",
        "fixture_type_point_in_time": "category",
        "current_vessel_sub_type_id_point_in_time": "category",
        "current_vessel_sub_type_point_in_time": "category",
    }


def test_places_static_data_columns_before_point_in_time_data_columns() -> None:
    all_columns = list(Column)

    is_static_column = lambda column: not column.endswith("point_in_time")
    static_data_columns = list(takewhile(is_static_column, all_columns))
    point_in_time_columns = list(dropwhile(is_static_column, all_columns))

    assert static_data_columns + point_in_time_columns == all_columns
