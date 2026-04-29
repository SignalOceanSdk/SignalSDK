"""Test cases derived from real Claude Desktop sessions."""
from dataclasses import dataclass, field


@dataclass
class TestCase:
    id: str
    question: str
    max_calls: int
    description: str = ""
    required_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    expected_answer: str = ""  # rubric for LLM-as-judge; empty = skip judge step


CASES: list[TestCase] = [
    # --- Composite tools ---
    TestCase(
        id="port_expenses_compare",
        question=(
            "Compare estimated port expenses for a Suezmax tanker at Rotterdam "
            "versus Fujairah — which port is cheaper?"
        ),
        max_calls=2,
        description="compare_port_expenses with vessel_class_name path",
        required_tools=["compare_port_expenses"],
        forbidden_tools=[
            "get_port_expenses_ports",
            "get_port_expenses_vessel_types",
            "get_vessel_classes",
            "get_port_model_vessel_expenses",
        ],
        expected_answer=(
            "States a specific cost figure (in USD) for both Rotterdam and Fujairah "
            "and names which one is cheaper."
        ),
    ),
    TestCase(
        id="tonnage_market_rates",
        question=(
            "What was the supply of MR2 tankers opening at ARA and the "
            "corresponding market rate on the MR2 Cont/USAC route over the "
            "last two weeks of March 2024?"
        ),
        max_calls=3,
        description="get_tonnage_list_and_market_rates composite",
        required_tools=["get_tonnage_list_and_market_rates"],
        forbidden_tools=["get_historical_tonnage_list", "get_market_rates"],
        expected_answer=(
            "Provides both a vessel count (tonnage supply) and a market rate value "
            "for MR2 tankers at ARA during the specified period."
        ),
    ),
    TestCase(
        id="distance_matrix",
        question=(
            "What are the sailing distances from Rotterdam to Ras Tanura, "
            "Singapore, Houston, and Fujairah for a laden VLCC?"
        ),
        max_calls=2,
        description="get_distance_matrix_from_port — one-origin many-destinations",
        required_tools=["get_distance_matrix_from_port"],
        forbidden_tools=["get_port_to_port_distance"],
        expected_answer=(
            "Provides nautical mile distances from Rotterdam to all four destinations: "
            "Ras Tanura, Singapore, Houston, and Fujairah."
        ),
    ),
    TestCase(
        id="aframax_valuations",
        question="What are the current estimated market values of Aframax tankers?",
        max_calls=3,
        description="get_vessel_valuations_for_class with staleness filter",
        required_tools=["get_vessel_valuations_for_class"],
        forbidden_tools=["get_vessels_by_vessel_class", "get_vessel_valuations_for_list"],
        expected_answer=(
            "Provides USD valuation figures for Aframax tankers, either as a range, "
            "average, or per-vessel breakdown."
        ),
    ),
    TestCase(
        id="emission_benchmark",
        question=(
            "How does the CII rating of the Nordic Odyssey compare to other "
            "Panamax tankers in 2024?"
        ),
        max_calls=3,
        description="get_vessel_emission_benchmark composite",
        required_tools=["get_vessel_emission_benchmark"],
        forbidden_tools=["get_vessel_emission_metrics", "get_vessel_class_emission_metrics"],
        expected_answer=(
            "States Nordic Odyssey's CII rating (letter A–E) and compares it to the "
            "Panamax fleet average or peer vessels, with AER or score values."
        ),
    ),
    TestCase(
        id="market_rate_vlcc",
        question="What is the current market rate for a VLCC on the MEG to China route?",
        max_calls=2,
        description="get_market_rates_by_route_name composite",
        required_tools=["get_market_rates_by_route_name"],
        forbidden_tools=["get_market_rate_routes", "get_market_rates"],
        expected_answer=(
            "Provides a specific rate value (Worldscale or TCE in USD/day) for the "
            "VLCC MEG-to-China route (TD3C or equivalent)."
        ),
    ),
    TestCase(
        id="operator_fleet",
        question="Can you tell me all EPS vessels?",
        max_calls=3,
        description="get_vessels_by_operator composite",
        required_tools=["get_vessels_by_operator"],
        forbidden_tools=["get_voyages_advanced_search", "get_vessels_by_vessel_class"],
        expected_answer=(
            "Lists multiple vessel names operated by EPS (Eastern Pacific Shipping), "
            "with vessel class or IMO numbers."
        ),
    ),

    # --- Vessel-specific chains ---
    TestCase(
        id="last_voyage_emissions",
        question=(
            "What was the last voyage of the Front Altair, and what were "
            "its CO2 emissions?"
        ),
        max_calls=3,
        description="get_latest_voyage_emissions composite (name → emissions)",
        required_tools=["get_latest_voyage_emissions"],
        expected_answer=(
            "Identifies Front Altair's most recent voyage (load and discharge ports or "
            "dates) and states CO2 emissions in tonnes for that voyage."
        ),
    ),
    TestCase(
        id="vessel_voyages_by_name",
        question="What voyages has the vessel Berge Bulk completed since the start of 2024?",
        max_calls=8,
        description="vessel name resolution + voyage history",
        required_tools=[],  # get_vessel_by_name or search_vessels are both valid for IMO lookup
        expected_answer=(
            "Lists multiple completed voyages for Berge Bulk since January 2024, "
            "each with load and/or discharge port names or dates."
        ),
    ),
    TestCase(
        id="vessel_eta",
        question="When is the Front Altair expected to arrive at Rotterdam?",
        max_calls=4,
        description="ETA via current voyage events",
        required_tools=[],  # either get_vessel_by_name or search_vessels is valid
        expected_answer=(
            "Provides a specific ETA (date or date-time) for Front Altair's arrival "
            "at Rotterdam, or explains why an ETA cannot be determined from available data."
        ),
    ),

    # --- Advanced search ---
    TestCase(
        id="advanced_voyage_search",
        question=(
            "Which Suezmax tankers loaded at Ras Tanura and discharged at "
            "Rotterdam between January and March 2024?"
        ),
        max_calls=3,
        description="get_voyages_advanced_search with port_name + vessel_class_name",
        required_tools=["get_voyages_advanced_search"],
        forbidden_tools=["get_tonnage_list_ports", "get_vessel_classes"],
        expected_answer=(
            "Lists one or more Suezmax vessel names (or IMO numbers) that completed "
            "a Ras Tanura → Rotterdam voyage in Q1 2024, or states none were found."
        ),
    ),

    # --- Scraped data discoverability ---
    TestCase(
        id="lineup_ras_tanura",
        question="Which tankers were reported in the lineup at Ras Tanura in the last 3 hours?",
        max_calls=8,  # may retry with different time windows if data is sparse
        description="get_scraped_lineups discoverability",
        required_tools=["get_scraped_lineups"],
        expected_answer=(
            "Returns lineup data from Ras Tanura — either lists vessel names/IMOs "
            "or states that no lineup reports were found in the timeframe."
        ),
    ),
    TestCase(
        id="vessel_position",
        question=(
            "Where is the Front Altair right now, and what position was "
            "last reported for it?"
        ),
        max_calls=5,
        description="scraped positions for a named vessel",
        required_tools=["get_scraped_positions"],
        expected_answer=(
            "Provides the last reported position of Front Altair — latitude/longitude "
            "or a port/area name — with a timestamp or date."
        ),
    ),

    # --- Combined notebook patterns ---
    TestCase(
        id="supply_vs_rates_vlcc",
        question=(
            "How did the number of VLCC tankers available at Ras Tanura correlate "
            "with the MEG/China market rate during Q1 2024?"
        ),
        max_calls=3,
        description="get_tonnage_list_and_market_rates — VLCC/MEG pattern",
        required_tools=["get_tonnage_list_and_market_rates"],
        expected_answer=(
            "Provides both VLCC supply counts at Ras Tanura and TD3C/MEG-China rate "
            "values during Q1 2024, and comments on any observed relationship."
        ),
    ),
]
