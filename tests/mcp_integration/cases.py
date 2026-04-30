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
        max_calls=3,
        description="get_market_rates_by_route_name composite",
        required_tools=["get_market_rates_by_route_name"],
        forbidden_tools=["get_market_rate_routes"],
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

    # =========================================================
    # Vessel Information (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="vessel_beneficial_owner",
        question="Who is the beneficial owner of DHT Leopard?",
        max_calls=3,
        description="vessel beneficial owner lookup by name",
        required_tools=[],
        expected_answer="Names the beneficial owner of DHT Leopard.",
    ),
    TestCase(
        id="vessel_particulars",
        question="When was DHT Leopard built and where?",
        max_calls=3,
        description="vessel build year and shipyard",
        required_tools=[],
        expected_answer="States DHT Leopard's build year and the country or shipyard where she was built.",
    ),
    TestCase(
        id="vessel_fuel_consumption",
        question="What is the fuel consumption of DHT Leopard?",
        max_calls=3,
        description="vessel fuel consumption via consumptions API",
        required_tools=["get_vessel_consumptions"],
        expected_answer="Provides fuel consumption figures for DHT Leopard at various speeds, in metric tons per day.",
    ),
    TestCase(
        id="vessel_operator",
        question="Who operates the vessel Seaking?",
        max_calls=3,
        description="vessel operator lookup by name",
        required_tools=[],
        expected_answer="Names the commercial operator of the vessel Seaking.",
    ),
    TestCase(
        id="vessel_dimensions",
        question="What are the dimensions of Eagle Barcelona?",
        max_calls=3,
        description="vessel length, beam, draft lookup",
        required_tools=[],
        expected_answer="Provides Eagle Barcelona's length, beam, or draft measurements.",
    ),
    TestCase(
        id="vessel_gross_tonnage",
        question="What is the gross tonnage of DHT Leopard?",
        max_calls=3,
        description="vessel gross tonnage lookup",
        required_tools=[],
        expected_answer="States DHT Leopard's gross tonnage in GT.",
    ),
    TestCase(
        id="vessel_class_lookup",
        question="What class of vessel is Seaking?",
        max_calls=3,
        description="vessel class lookup by name",
        required_tools=[],
        expected_answer="Names the vessel class of Seaking (e.g. VLCC, Suezmax, Aframax).",
    ),

    # =========================================================
    # Voyage History & Canal Crossings (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="voyage_canal_crossings_panama",
        question="Did Philotimos transit the Panama Canal on the last 10 voyages? Did it cross in the ballast or laden leg?",
        max_calls=5,
        description="Panama Canal transit detection across voyage history",
        required_tools=[],
        expected_answer="States whether Philotimos transited the Panama Canal in its last 10 voyages and, if so, whether crossings occurred on ballast or laden legs.",
    ),
    TestCase(
        id="voyage_load_discharge_ports",
        question="Where did Seaking load and discharge cargo in its last 3 voyages?",
        max_calls=5,
        description="load/discharge port history for named vessel",
        required_tools=[],
        expected_answer="Lists load and discharge ports for the last 3 voyages of Seaking.",
    ),
    TestCase(
        id="voyage_cargo_type",
        question="What cargo type and grade did vessel IMO 9795048 carry on its most recent voyage?",
        max_calls=4,
        description="cargo type/grade from latest voyage by IMO",
        required_tools=[],
        expected_answer="States the cargo type and grade for vessel IMO 9795048's most recent voyage.",
    ),
    TestCase(
        id="vessel_current_voyage",
        question="What is the current voyage of MT Nordic Hawk?",
        max_calls=4,
        description="current or most recent voyage for named vessel",
        required_tools=[],
        expected_answer="Describes MT Nordic Hawk's current or most recent voyage, including load or discharge port or voyage status.",
    ),
    TestCase(
        id="vessel_ports_visited",
        question="Which ports has vessel IMO 9795048 visited in its recent voyages?",
        max_calls=4,
        description="port visit history by IMO",
        required_tools=["get_voyages"],
        expected_answer="Lists port names visited by vessel IMO 9795048 in recent voyages.",
    ),
    TestCase(
        id="voyage_charterer_search",
        question="Has Arachthos I conducted any voyages for Aramco in the last two years?",
        max_calls=6,
        description="voyage search filtered by charterer for a named vessel",
        required_tools=[],  # get_voyages_advanced_search preferred but get_voyages also valid
        expected_answer="States whether Arachthos I has conducted voyages for Aramco in the past two years, with voyage details if found.",
    ),

    # =========================================================
    # Voyage Analytics (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="voyage_analytics_suezmax_usgulf_operators",
        question="Which operators had the most Suezmax loading events in the US Gulf in Q4 2025?",
        max_calls=5,
        description="Suezmax operator ranking by loading events in US Gulf Q4 2025 (partial)",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Lists commercial operators ranked by Suezmax loading events in the US Gulf during Q4 2025, with counts or ranks.",
    ),
    TestCase(
        id="voyage_analytics_ag_crude",
        question="Give me all the vessels that loaded crude oil from the AG in the last week",
        max_calls=4,
        description="crude oil loadings from Arabian Gulf last week",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Lists vessel names or IMOs that loaded crude oil from the Arabian Gulf in the past week, or states none were found.",
    ),
    TestCase(
        id="voyage_analytics_vlcc_rotterdam",
        question="Show me the monthly VLCC discharge events in Rotterdam over the past year",
        max_calls=4,
        description="monthly VLCC discharge aggregation at Rotterdam",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Provides VLCC discharge event counts at Rotterdam by month over the past year, or a total count.",
    ),
    TestCase(
        id="voyage_analytics_aframax_nwe",
        question="How many Aframax loadings were there in Northwest Europe last month?",
        max_calls=5,
        description="Aframax loading count in NWE last month",
        required_tools=[],  # get_voyages_advanced_search or get_voyages_flat are both valid
        expected_answer="Provides a count of Aframax loading events in Northwest Europe in the previous month.",
    ),
    TestCase(
        id="voyage_analytics_vlcc_ag_forecast",
        question="How many VLCC loadings are forecasted in the Arabian Gulf in the next 2 weeks?",
        max_calls=6,
        description="VLCC loading forecast in Arabian Gulf",
        required_tools=[],  # multiple tools are valid for forecasting
        expected_answer="Provides a count or list of forecasted VLCC loading events in the Arabian Gulf over the next 2 weeks.",
    ),
    TestCase(
        id="voyage_analytics_sts",
        question="How many ship-to-ship transfer operations took place worldwide in the last 90 days?",
        max_calls=4,
        description="global STS operation count",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Provides a count of ship-to-ship (STS) transfer operations worldwide in the past 90 days.",
    ),

    # =========================================================
    # Market Rates (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="market_rates_dry_bulk_routes",
        question="What dry bulk market rate routes can I track?",
        max_calls=3,
        description="dry bulk route discovery via get_market_rate_routes",
        required_tools=["get_market_rate_routes"],
        expected_answer="Lists available dry bulk market rate routes (e.g. C5TC, C3, BCI, P5TC) that can be tracked.",
    ),
    TestCase(
        id="market_rates_capesize",
        question="What are the current Capesize rates?",
        max_calls=8,
        description="current Capesize dry bulk market rates",
        required_tools=[],
        expected_answer="Provides current rate values (USD/day or index points) for Capesize bulk carrier routes.",
    ),
    TestCase(
        id="market_rates_clean_tanker",
        question="Show me clean tanker spot rates",
        max_calls=12,
        description="clean product tanker spot rates",
        required_tools=[],
        expected_answer="Provides current spot rate values for clean tanker routes (e.g. TC2, TC5, or MR routes).",
    ),
    TestCase(
        id="market_rates_bci",
        question="Show me BCI over the last year",
        max_calls=5,
        description="Baltic Capesize Index timeseries",
        required_tools=[],  # get_market_rates or get_market_rates_by_route_name are both valid
        expected_answer="Provides BCI (Baltic Capesize Index) values over the past year as a timeseries or summary.",
    ),
    TestCase(
        id="market_rates_td3c_td20",
        question="Compare TD3C and TD20 side by side",
        max_calls=5,
        description="comparison of two tanker rate routes",
        required_tools=[],  # get_market_rates or get_market_rates_by_route_name are both valid
        expected_answer="Provides rate values for both TD3C (VLCC MEG-China) and TD20 (Suezmax West Africa) for comparison.",
    ),
    TestCase(
        id="market_rates_dry_bulk_overview",
        question="Give me a dry bulk market overview",
        max_calls=10,
        description="dry bulk market rates across vessel classes",
        required_tools=[],
        expected_answer="Provides an overview of dry bulk market rates covering at least two vessel classes (Capesize, Panamax, or Supramax).",
    ),

    # =========================================================
    # Live Availability & Tonnage (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="tonnage_capesize_open_position",
        question="Where does Capesize vessel Cape Amal open?",
        max_calls=5,
        description="single Capesize vessel open position and port",
        required_tools=[],
        expected_answer="States where Cape Amal is next open (port or area) and an open date, or explains it cannot be determined.",
    ),
    TestCase(
        id="tonnage_vlcc_ag",
        question="VLCCs opening in AG next 30 days",
        max_calls=4,
        description="live VLCC availability in Arabian Gulf",
        required_tools=["get_tonnage_list"],
        expected_answer="Lists VLCC vessels opening in the Arabian Gulf in the next 30 days, with vessel names or open dates.",
    ),
    TestCase(
        id="tonnage_suezmax_waf",
        question="Show me the Suezmax tonnage list for West Africa",
        max_calls=4,
        description="Suezmax tonnage list for West Africa",
        required_tools=["get_tonnage_list"],
        expected_answer="Lists Suezmax vessels available at or opening for West Africa, with vessel names or open dates.",
    ),
    TestCase(
        id="tonnage_vessel_open_date",
        question="When does DHT Leopard open?",
        max_calls=5,
        description="single vessel next open position",
        required_tools=[],
        expected_answer="States when and where DHT Leopard is next available (open date and port), or explains it cannot be determined.",
    ),
    TestCase(
        id="tonnage_vlcc_arabian_gulf",
        question="Show me VLCCs open in the Arabian Gulf",
        max_calls=4,
        description="open VLCCs in Arabian Gulf",
        required_tools=["get_tonnage_list"],
        expected_answer="Lists VLCC vessels currently open or opening soon in the Arabian Gulf.",
    ),
    TestCase(
        id="tonnage_lng_available",
        question="Find available LNG carriers",
        max_calls=6,
        description="available LNG carrier tonnage list",
        required_tools=["get_tonnage_list"],
        expected_answer="Lists LNG carrier vessels that are currently available or opening soon.",
    ),

    # =========================================================
    # Distances & Routing (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="eta_imo_fujairah_sea_margin",
        question="Calculate ETA for vessel IMO 9745902 to Fujairah with 3% sea margin",
        max_calls=5,
        description="ETA calculation by IMO with sea margin",
        required_tools=[],
        expected_answer="Provides an ETA (date or date-time) for vessel IMO 9745902 to reach Fujairah, incorporating a 3% sea margin.",
    ),
    TestCase(
        id="distance_rotterdam_singapore",
        question="What is the distance from Rotterdam to Singapore?",
        max_calls=2,
        description="point-to-point sailing distance",
        required_tools=["get_port_to_port_distance"],
        forbidden_tools=["get_distance_matrix_from_port"],
        expected_answer="Provides the sailing distance in nautical miles from Rotterdam to Singapore.",
    ),
    TestCase(
        id="distance_houston_rotterdam_vlcc",
        question="Calculate the distance from Houston to Rotterdam for a VLCC tanker",
        max_calls=2,
        description="VLCC sailing distance between two ports",
        required_tools=["get_port_to_port_distance"],
        forbidden_tools=["get_distance_matrix_from_port"],
        expected_answer="Provides the sailing distance in nautical miles from Houston to Rotterdam for a VLCC.",
    ),
    TestCase(
        id="distance_ras_tanura_fujairah",
        question="What is the distance from Ras Tanura to Fujairah?",
        max_calls=2,
        description="Gulf port-to-port distance",
        required_tools=["get_port_to_port_distance"],
        forbidden_tools=["get_distance_matrix_from_port"],
        expected_answer="Provides the sailing distance in nautical miles from Ras Tanura to Fujairah.",
    ),
    TestCase(
        id="route_houston_rotterdam",
        question="Show me the route details from Houston to Rotterdam for a VLCC",
        max_calls=3,
        description="route with waypoints and canal info",
        required_tools=["get_port_to_port_route"],
        expected_answer="Provides route details from Houston to Rotterdam for a VLCC, including total distance and key waypoints or canals transited.",
    ),
    TestCase(
        id="route_alternatives_singapore_fujairah",
        question="What are the alternative routes from Singapore to Fujairah?",
        max_calls=4,
        description="alternative route options between two ports",
        required_tools=[],
        expected_answer="Lists multiple route options from Singapore to Fujairah with distances, including via Malacca Strait and any alternative passages.",
    ),

    # =========================================================
    # Fixtures & Chartering (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="fixtures_tanker_discharge_china_q4_2025",
        question="How many tanker fixtures discharged in China in Q4 2025?",
        max_calls=6,
        description="tanker fixture count by discharge area Q4 2025 (partial)",
        required_tools=["get_voyage_market_data_advanced"],
        expected_answer="Provides a count of tanker fixtures with discharge in China during Q4 2025.",
    ),
    TestCase(
        id="fixtures_lng_q4_2025",
        question="Show me LNG fixtures with lumpsum rates in Q4 2025",
        max_calls=12,
        description="scraped LNG fixtures with lumpsum rate filter",
        required_tools=["get_scraped_fixtures"],
        expected_answer="Lists LNG carrier fixtures from Q4 2025 with lumpsum rate details, or states none were found.",
    ),
    TestCase(
        id="fixtures_suezmax_jan_2026",
        question="List the 10 most recent Suezmax fixtures in January 2026.",
        max_calls=8,
        description="class-filtered fixture listing",
        required_tools=["get_voyage_market_data_advanced"],
        expected_answer="Lists up to 10 Suezmax fixture records from January 2026 with charterer, load port, or rate information.",
    ),
    TestCase(
        id="fixtures_vlcc_laycan_march_2026",
        question="How many fully fixed VLCC fixtures have laycan dates in March 2026?",
        max_calls=8,
        description="VLCC fixture count by laycan date range",
        required_tools=["get_voyage_market_data_advanced"],
        expected_answer="Provides a count of fully fixed VLCC fixtures with laycan dates in March 2026.",
    ),
    TestCase(
        id="fixtures_top_charterers_vlcc_2025",
        question="Who are the top 10 charterers for VLCC fixtures in 2025?",
        max_calls=8,
        description="top VLCC charterers by fixture count (partial)",
        required_tools=["get_voyage_market_data_advanced"],
        expected_answer="Lists charterer names ranked by VLCC fixture activity in 2025, with counts or ranks.",
    ),
    TestCase(
        id="fixtures_suezmax_ws_rates",
        question="What are the average, minimum, and maximum WS rates across Suezmax fixtures in Q1 2025?",
        max_calls=8,
        description="Suezmax fixture WS rate statistics (partial — Claude aggregates)",
        required_tools=[],
        expected_answer="Provides average, minimum, and maximum Worldscale rates from Suezmax fixtures in Q1 2025.",
    ),

    # =========================================================
    # Fleet Analytics (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="fleet_suezmax_age_brackets",
        question="Break down the Suezmax fleet by age brackets: 0-5, 5-10, 10-15, 15-20, and 20+ years.",
        max_calls=4,
        description="Suezmax fleet age bracket breakdown (partial — Claude aggregates)",
        required_tools=["get_vessels_by_vessel_class"],
        expected_answer="Provides vessel counts for the Suezmax fleet grouped by age brackets (0-5, 5-10, 10-15, 15-20, 20+ years).",
    ),
    TestCase(
        id="fleet_scorpio_tankers",
        question="List all tankers operated by Scorpio Tankers",
        max_calls=4,
        description="fleet listing by operator name",
        required_tools=["get_vessels_by_operator"],
        expected_answer="Lists vessel names or IMOs operated by Scorpio Tankers, with vessel class or type.",
    ),
    TestCase(
        id="fleet_vlcc_scrubbers_count",
        question="How many VLCCs have scrubbers fitted?",
        max_calls=4,
        description="VLCC scrubber count (partial)",
        required_tools=["get_vessels_by_vessel_class"],
        expected_answer="Provides a count of VLCCs fitted with scrubbers.",
    ),
    TestCase(
        id="fleet_liberian_vlccs",
        question="How many Liberian-flagged VLCCs are there in the global fleet?",
        max_calls=4,
        description="VLCC count by flag state (partial)",
        required_tools=["get_vessels_by_vessel_class"],
        expected_answer="Provides a count of Liberian-flagged VLCCs in the global fleet.",
    ),
    TestCase(
        id="fleet_aframax_built_2010_2020",
        question="Find Aframax tankers built between 2010 and 2020",
        max_calls=4,
        description="Aframax fleet filtered by build year (partial)",
        required_tools=["get_vessels_by_vessel_class"],
        expected_answer="Lists Aframax tankers built between 2010 and 2020, with vessel names, IMOs, or build years.",
    ),
    TestCase(
        id="fleet_aframax_scrubbers",
        question="List all Aframax tankers that are fitted with Scrubbers.",
        max_calls=4,
        description="Aframax fleet filtered by scrubber equipment (partial)",
        required_tools=["get_vessels_by_vessel_class"],
        expected_answer="Lists Aframax tankers fitted with scrubbers, with vessel names or IMOs.",
    ),

    # =========================================================
    # Port Insights (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="port_aframax_scrubbers_rotterdam",
        question="How many Aframax tankers with scrubbers called at Rotterdam last month?",
        max_calls=5,
        description="Aframax calls at Rotterdam filtered by scrubber equipment (partial)",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Provides a count of Aframax tankers with scrubbers that called at Rotterdam in the previous month.",
    ),
    TestCase(
        id="port_aframax_calls",
        question="How many Aframax tankers loaded at Rotterdam in the last 30 days?",
        max_calls=4,
        description="Aframax loading count at Rotterdam",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Provides a count or list of Aframax tanker loading events at Rotterdam in the past 30 days.",
    ),
    TestCase(
        id="port_terminals_fujairah",
        question="List all terminals at Fujairah",
        max_calls=3,
        description="port terminal listing via geo assets",
        required_tools=["get_geo_assets"],
        expected_answer="Lists terminal names or facilities at Fujairah, or states the data is unavailable.",
    ),
    TestCase(
        id="port_operators_singapore_vlcc",
        question="Which commercial operators call at Singapore most frequently for VLCC tankers",
        max_calls=4,
        description="operator frequency at Singapore for VLCCs (partial)",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Lists commercial operators by frequency of VLCC calls at Singapore, or provides counts per operator.",
    ),
    TestCase(
        id="port_europoort_calls",
        question="How many tankers called at the Europoort terminal in Rotterdam over the past year?",
        max_calls=4,
        description="tanker call count at Europoort",
        required_tools=["get_voyages_advanced_search"],
        expected_answer="Provides a count of tanker port calls at the Europoort terminal in Rotterdam over the past year.",
    ),
    TestCase(
        id="port_suezmax_operators_fujairah",
        question="Show me the top operators for Suezmax tankers at Fujairah",
        max_calls=5,
        description="Suezmax operator ranking at Fujairah (partial)",
        required_tools=[],  # get_voyages_advanced_search or get_tonnage_list are both reasonable
        expected_answer="Lists commercial operators ranked by Suezmax tanker activity at Fujairah.",
    ),

    # =========================================================
    # Emissions & CII (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="vlcc_valuations_q4_2025",
        question="What is the current average VLCC valuation?",
        max_calls=3,
        description="VLCC fleet valuation statistics via composite tool",
        required_tools=["get_vessel_valuations_for_class"],
        expected_answer="Provides current average VLCC vessel valuation figures (in USD million).",
    ),
    TestCase(
        id="cii_rating_dht_leopard",
        question="What is the CII rating for DHT Leopard?",
        max_calls=3,
        description="CII rating for a specific vessel",
        required_tools=["get_vessel_emission_metrics"],
        expected_answer="States DHT Leopard's CII rating (letter A–E) and/or CII score for the most recent year.",
    ),

    # =========================================================
    # Port Expenses (from SUPPORTED_QUESTIONS.md)
    # =========================================================
    TestCase(
        id="port_expenses_vlcc_ras_tanura",
        question="What are the port expenses for a VLCC loading at Ras Tanura?",
        max_calls=8,
        description="port expenses for VLCC at Ras Tanura",
        required_tools=[],  # compare_port_expenses or get_port_model_vessel_expenses are both valid
        forbidden_tools=[],
        expected_answer="Provides estimated port expenses in USD for a VLCC loading at Ras Tanura.",
    ),
    TestCase(
        id="port_expenses_aframax_rotterdam",
        question="How much would an Aframax pay for a discharge call at Rotterdam?",
        max_calls=8,
        description="port expenses for Aframax at Rotterdam",
        required_tools=[],  # compare_port_expenses or get_port_model_vessel_expenses are both valid
        forbidden_tools=[],
        expected_answer="Provides estimated port expenses in USD for an Aframax discharge call at Rotterdam.",
    ),
]
