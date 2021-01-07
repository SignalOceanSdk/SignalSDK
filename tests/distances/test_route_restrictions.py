import pytest

from signal_ocean.distances import RouteRestrictions

DEFAULT_QUERY_STRING = {
    "IsSuezOpen": None,
    "IsPanamaOpen": None,
    "IsMessinaOpen": None,
    "IsOresundOpen": None,
    "IsSuezOpenOnlyNorthbound": None,
    "IsPiracyConsidered": None,
}


def test_converts_to_query_string_with_default_values():
    restrictions = RouteRestrictions()

    query_string = restrictions._to_query_string()

    assert query_string == DEFAULT_QUERY_STRING


@pytest.mark.parametrize(
    "parameters, expected_overrides",
    [
        ({"is_suez_open": True}, {"IsSuezOpen": True}),
        ({"is_panama_open": True}, {"IsPanamaOpen": True}),
        ({"is_messina_open": True}, {"IsMessinaOpen": True}),
        ({"is_oresund_open": True}, {"IsOresundOpen": True}),
        ({"is_piracy_considered": True}, {"IsPiracyConsidered": True}),
        (
            {"is_suez_open_only_northbound": True},
            {"IsSuezOpenOnlyNorthbound": True},
        ),
        ({"is_suez_open": False}, {"IsSuezOpen": False}),
        ({"is_panama_open": False}, {"IsPanamaOpen": False}),
        ({"is_messina_open": False}, {"IsMessinaOpen": False}),
        ({"is_oresund_open": False}, {"IsOresundOpen": False}),
        ({"is_piracy_considered": False}, {"IsPiracyConsidered": False}),
        (
            {"is_suez_open_only_northbound": False},
            {"IsSuezOpenOnlyNorthbound": False},
        ),
    ],
)
def test_overrides_query_string_defaults_with_specified_parameters(
    parameters, expected_overrides
):
    restrictions = RouteRestrictions(**parameters)

    query_string = restrictions._to_query_string()

    expected_query_string = {**DEFAULT_QUERY_STRING, **expected_overrides}
    assert query_string == expected_query_string
