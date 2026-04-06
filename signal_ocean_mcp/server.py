"""Signal Ocean MCP Server.

Exposes Signal Ocean SDK APIs as MCP tools for use with
Claude and other MCP-compatible AI clients.
"""

import json
from datetime import date, datetime
from typing import Any, List, Optional

from mcp.server.fastmcp import FastMCP

from signal_ocean.connection import Connection
from signal_ocean.companies.companies_api import CompaniesAPI
from signal_ocean.distances.distances_api import DistancesAPI
from signal_ocean.freight_pricing.freight_pricing_api import FreightPricingAPI
from signal_ocean.freight_rates.freight_rates_api import FreightRatesAPI
from signal_ocean.geos.geos_api import GeosAPI
from signal_ocean.historical_tonnage_list.historical_tonnage_list_api import (
    HistoricalTonnageListAPI,
)
from signal_ocean.market_rates.market_rates_api import MarketRatesAPI
from signal_ocean.port_expenses.port_expenses_api import PortExpensesAPI
from signal_ocean.tonnage_list.api import TonnageListAPI
from signal_ocean.vessel_emissions.vessel_emissions_api import (
    VesselEmissionsAPI,
)
from signal_ocean.vessel_valuations.vessel_valuations_api import (
    VesselValuationsAPI,
)
from signal_ocean.vessels.vessels_api import VesselsAPI
from signal_ocean.voyages.voyages_api import VoyagesAPI
from signal_ocean.voyages_market_data.voyages_market_data_api import (
    VoyagesMarketDataAPI,
)
from signal_ocean.scraped_cargoes.scraped_cargoes_api import ScrapedCargoesAPI
from signal_ocean.scraped_fixtures.scraped_fixtures_api import (
    ScrapedFixturesAPI,
)
from signal_ocean.scraped_lineups.scraped_lineups_api import ScrapedLineupsAPI
from signal_ocean.scraped_positions.scraped_positions_api import (
    ScrapedPositionsAPI,
)
from signal_ocean.vessel_consumptions.vessel_consumptions_api import (
    VesselConsumptionsAPI,
)

mcp = FastMCP(
    "Signal Ocean",
    instructions=(
        "Signal Ocean provides maritime shipping data APIs. "
        "Use these tools to query vessel information, voyages, "
        "emissions, market rates, freight pricing, distances, "
        "port expenses, tonnage lists, and scraped market data. "
        "All tools require a valid Signal Ocean API key configured "
        "via the SIGNAL_OCEAN_API_KEY environment variable."
    ),
)


def _connection() -> Connection:
    return Connection()


def _serialize(obj: Any) -> str:
    """Serialize SDK response objects to JSON strings."""
    if obj is None:
        return json.dumps(None)
    if isinstance(obj, (list, tuple)):
        return json.dumps(
            [_to_dict(item) for item in obj], default=str
        )
    return json.dumps(_to_dict(obj), default=str)


def _to_dict(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", by_alias=True)
    # Handle Sequence-like objects (e.g. HistoricalTonnageList)
    # that support len/iteration but store data in mangled attrs.
    if hasattr(obj, "__len__") and hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, dict)):
        items = list(obj)
        if items:
            return [_to_dict(item) for item in items]
        # For wrapper objects, also check for public attributes
        public = {k: v for k, v in obj.__dict__.items()
                  if not k.startswith("_")}
        if public:
            return public
        return []
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items()
                if not k.startswith("_")}
    return obj


def _parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    return date.fromisoformat(value)


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value)


# --- Vessel Lookup (via Voyages API) ---


@mcp.tool()
def search_vessel_imos(name: Optional[str] = None) -> str:
    """Search for vessel IMO numbers by name.

    Returns vessels with their IMO and name. Use this to find
    a vessel's IMO before querying voyages or other APIs.
    """
    from signal_ocean.voyages.voyages_api import VoyagesAPI as VoyAPI
    from signal_ocean.voyages.models import VesselFilter

    api = VoyAPI(_connection())
    vf = VesselFilter(name_like=name) if name else None
    return _serialize(api.get_imos(vf))


# --- Vessels ---


@mcp.tool()
def get_vessel(imo: int) -> str:
    """Get detailed information about a specific vessel by its IMO number."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessel(imo))


@mcp.tool()
def search_vessels(name: Optional[str] = None) -> str:
    """Search for vessels by name. Returns all vessels if no name given."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessels(name=name))


@mcp.tool()
def get_vessels_by_vessel_class(vessel_class_id: int) -> str:
    """Get all vessels belonging to a specific vessel class.

    Use get_vessel_classes to find available vessel class IDs.
    """
    api = VesselsAPI(_connection())
    return _serialize(
        api.get_vessels_by_vessel_class(vesselClass=vessel_class_id)
    )


@mcp.tool()
def get_vessel_classes() -> str:
    """Get all available vessel classes (e.g., Capesize, VLCC, etc.)."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessel_classes())


@mcp.tool()
def get_vessel_types() -> str:
    """Get all available vessel types (e.g., Tanker, Dry Bulk, etc.)."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessel_types())


@mcp.tool()
def get_vessel_name_history(imo: int) -> str:
    """Get the name history for a vessel by IMO number."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessels_name_history(imo=imo))


@mcp.tool()
def get_vessel_commercial_operator_history(imo: int) -> str:
    """Get the commercial operator history for a vessel by IMO number."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessels_commOp_history(imo=imo))


@mcp.tool()
def get_vessel_flag_history(imo: int) -> str:
    """Get the flag (country of registration) history for a vessel by IMO."""
    api = VesselsAPI(_connection())
    return _serialize(api.get_vessels_flag_history(imo=imo))


# --- Vessel Emissions ---


@mcp.tool()
def get_vessel_emissions(
    imo: int,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = False,
    include_distances: bool = False,
    include_durations: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions data for a vessel by IMO number.

    Returns emission estimations for all voyages of the vessel.
    """
    api = VesselEmissionsAPI(_connection())
    return _serialize(
        api.get_emissions_by_imo(
            imo,
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_eu_emissions=include_eu_emissions,
        )
    )


@mcp.tool()
def get_voyage_emissions(
    imo: int,
    voyage_number: int,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = False,
    include_distances: bool = False,
    include_durations: bool = False,
    include_speed_statistics: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions data for a specific voyage of a vessel."""
    api = VesselEmissionsAPI(_connection())
    return _serialize(
        api.get_emissions_by_imo_and_voyage_number(
            imo=imo,
            voyage_number=voyage_number,
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_speed_statistics=include_speed_statistics,
            include_eu_emissions=include_eu_emissions,
        )
    )


@mcp.tool()
def get_vessel_class_emissions(
    vessel_class_id: int,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = False,
    include_distances: bool = False,
    include_durations: bool = False,
    include_speed_statistics: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions data for all vessels in a vessel class."""
    api = VesselEmissionsAPI(_connection())
    return _serialize(
        api.get_emissions_by_vessel_class_id(
            vessel_class_id=vessel_class_id,
            include_consumptions=include_consumptions,
            include_efficiency_metrics=include_efficiency_metrics,
            include_distances=include_distances,
            include_durations=include_durations,
            include_speed_statistics=include_speed_statistics,
            include_eu_emissions=include_eu_emissions,
        )
    )


@mcp.tool()
def get_vessel_emission_metrics(
    imo: int, year: Optional[int] = None
) -> str:
    """Get emission metrics (CII, AER, EEOI) for a vessel by IMO."""
    api = VesselEmissionsAPI(_connection())
    return _serialize(api.get_metrics_by_imo(imo, year=year))


@mcp.tool()
def get_vessel_class_emission_metrics(
    vessel_class_id: int, year: Optional[int] = None
) -> str:
    """Get emission metrics (CII, AER, EEOI) for all vessels in a class."""
    api = VesselEmissionsAPI(_connection())
    return _serialize(
        api.get_metrics_by_vessel_class_id(
            vessel_class_id=vessel_class_id, year=year
        )
    )


# --- Vessel Consumptions ---


@mcp.tool()
def get_vessel_consumptions(imo: int) -> str:
    """Get fuel consumption data for a vessel by IMO number."""
    api = VesselConsumptionsAPI(_connection())
    return _serialize(api.get_consumptions(imo))


@mcp.tool()
def get_vessel_advertised_consumptions(imo: int) -> str:
    """Get advertised (reported) fuel consumption data for a vessel."""
    api = VesselConsumptionsAPI(_connection())
    return _serialize(api.get_advertised_consumptions(imo))


# --- Vessel Valuations ---


@mcp.tool()
def get_vessel_valuation(imo: int) -> str:
    """Get the latest valuation for a vessel by IMO number."""
    api = VesselValuationsAPI(_connection())
    return _serialize(api.get_latest_valuation_by_imo(imo))


@mcp.tool()
def get_vessel_historical_valuations(
    imo: int,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    """Get historical valuations for a vessel. Dates as YYYY-MM-DD."""
    api = VesselValuationsAPI(_connection())
    return _serialize(
        api.get_all_historical_valuations_by_imo(
            imo, from_date=from_date, to_date=to_date
        )
    )


@mcp.tool()
def get_vessel_valuations_for_list(imo_list: list[int]) -> str:
    """Get latest valuations for multiple vessels at once.

    Pass a list of IMO numbers.
    """
    api = VesselValuationsAPI(_connection())
    return _serialize(
        api.get_latest_valuations_for_list_of_vessels(imo_list)
    )


@mcp.tool()
def get_vessel_valuations_paged(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    changed_since: Optional[str] = None,
) -> str:
    """Get latest valuations for all vessels, paginated.

    changed_since as YYYY-MM-DD to get only recently updated valuations.
    """
    api = VesselValuationsAPI(_connection())
    return _serialize(
        api.get_latest_valuations_by_page(
            page=page, page_size=page_size, changed_since=changed_since
        )
    )


# --- Voyages ---


@mcp.tool()
def get_voyages(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyage data for vessels.

    Filter by IMO, vessel class ID, vessel type ID, or start date
    (YYYY-MM-DD). At least one filter is recommended to limit results.
    """
    api = VoyagesAPI(_connection())
    return _serialize(
        api.get_voyages(
            imo=imo,
            vessel_class_id=vessel_class_id,
            vessel_type_id=vessel_type_id,
            date_from=_parse_date(date_from),
        )
    )


@mcp.tool()
def get_voyages_condensed(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get condensed voyage data (lighter payload than full voyages)."""
    api = VoyagesAPI(_connection())
    return _serialize(
        api.get_voyages_condensed(
            imo=imo,
            vessel_class_id=vessel_class_id,
            vessel_type_id=vessel_type_id,
            date_from=_parse_date(date_from),
        )
    )


@mcp.tool()
def get_voyages_flat(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyages in flat format (separate lists for voyages, events, details, geos).

    Useful for large datasets as it avoids deeply nested structures.
    """
    api = VoyagesAPI(_connection())
    return _serialize(
        api.get_voyages_flat(
            imo=imo,
            vessel_class_id=vessel_class_id,
            vessel_type_id=vessel_type_id,
            date_from=_parse_date(date_from),
        )
    )


@mcp.tool()
def get_voyages_advanced_search(
    imos: Optional[list[int]] = None,
    vessel_class_id: Optional[int] = None,
    vessel_class_ids: Optional[list[int]] = None,
    vessel_type_id: Optional[int] = None,
    port_id: Optional[int] = None,
    port_ids: Optional[list[int]] = None,
    commercial_operator_id: Optional[int] = None,
    charterer_id: Optional[int] = None,
    start_date_from: Optional[str] = None,
    start_date_to: Optional[str] = None,
    first_load_arrival_date_from: Optional[str] = None,
    first_load_arrival_date_to: Optional[str] = None,
    end_date_from: Optional[str] = None,
    end_date_to: Optional[str] = None,
    event_type: Optional[int] = None,
    event_purpose: Optional[str] = None,
    event_horizon: Optional[int] = None,
    voyage_horizon: Optional[str] = None,
    hide_event_details: Optional[bool] = None,
    hide_events: Optional[bool] = None,
    hide_market_info: Optional[bool] = None,
) -> str:
    """Advanced voyage search with many filter options.

    Supports filtering by multiple IMOs, vessel classes, ports,
    charterers, operators, date ranges, event types, and more.
    Dates as YYYY-MM-DD.
    """
    api = VoyagesAPI(_connection())
    return _serialize(
        api.get_voyages_by_advanced_search(
            imos=imos,
            vessel_class_id=vessel_class_id,
            vessel_class_ids=vessel_class_ids,
            vessel_type_id=vessel_type_id,
            port_id=port_id,
            port_ids=port_ids,
            commercial_operator_id=commercial_operator_id,
            charterer_id=charterer_id,
            start_date_from=_parse_date(start_date_from),
            start_date_to=_parse_date(start_date_to),
            first_load_arrival_date_from=_parse_date(
                first_load_arrival_date_from
            ),
            first_load_arrival_date_to=_parse_date(
                first_load_arrival_date_to
            ),
            end_date_from=_parse_date(end_date_from),
            end_date_to=_parse_date(end_date_to),
            event_type=event_type,
            event_purpose=event_purpose,
            event_horizon=event_horizon,
            voyage_horizon=voyage_horizon,
            hide_event_details=hide_event_details,
            hide_events=hide_events,
            hide_market_info=hide_market_info,
        )
    )


# --- Voyages Market Data ---


@mcp.tool()
def get_voyage_market_data(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    include_vessel_details: bool = False,
    include_fixtures: bool = False,
    include_matched_fixture: bool = False,
    include_labels: bool = False,
) -> str:
    """Get market data associated with voyages.

    Includes fixture information, freight rates, and market context.
    """
    api = VoyagesMarketDataAPI(_connection())
    return _serialize(
        api.get_voyage_market_data(
            imo=imo,
            vessel_class_id=vessel_class_id,
            vessel_type_id=vessel_type_id,
            include_vessel_details=include_vessel_details,
            include_fixtures=include_fixtures,
            include_matched_fixture=include_matched_fixture,
            include_labels=include_labels,
        )
    )


@mcp.tool()
def get_voyage_market_data_advanced(
    imos: Optional[list[int]] = None,
    vessel_class_ids: Optional[list[int]] = None,
    trade_id: Optional[int] = None,
    include_vessel_details: Optional[bool] = None,
    include_fixtures: Optional[bool] = None,
    include_lineups: Optional[bool] = None,
    include_positions: Optional[bool] = None,
    include_matched_fixture: Optional[bool] = None,
    filter_by_matched_fixture: Optional[bool] = None,
    fixture_date_from: Optional[str] = None,
    fixture_date_to: Optional[str] = None,
    laycan_date_from: Optional[str] = None,
    laycan_date_to: Optional[str] = None,
    include_labels: Optional[bool] = None,
    charterer_ids_include: Optional[list[int]] = None,
    charterer_ids_exclude: Optional[list[int]] = None,
    cargo_type_ids_include: Optional[list[int]] = None,
    cargo_type_ids_exclude: Optional[list[int]] = None,
) -> str:
    """Advanced voyage market data search with filtering.

    Filter by multiple IMOs, vessel classes, trades, charterers,
    cargo types, fixture dates, and laycan dates. Dates as YYYY-MM-DD.
    """
    api = VoyagesMarketDataAPI(_connection())
    # Pass date strings directly — the SDK POST body serializes via
    # json.dumps which cannot handle date objects.
    return _serialize(
        api.get_voyage_market_data_advanced(
            imos=imos,
            vessel_class_ids=vessel_class_ids,
            trade_id=trade_id,
            include_vessel_details=include_vessel_details,
            include_fixtures=include_fixtures,
            include_lineups=include_lineups,
            include_positions=include_positions,
            include_matched_fixture=include_matched_fixture,
            filter_by_matched_fixture=filter_by_matched_fixture,
            fixture_date_from=fixture_date_from,
            fixture_date_to=fixture_date_to,
            laycan_date_from=laycan_date_from,
            laycan_date_to=laycan_date_to,
            include_labels=include_labels,
            charterer_ids_include=charterer_ids_include,
            charterer_ids_exclude=charterer_ids_exclude,
            cargo_type_ids_include=cargo_type_ids_include,
            cargo_type_ids_exclude=cargo_type_ids_exclude,
        )
    )


# --- Market Rates ---


@mcp.tool()
def get_market_rates(
    start_date: str,
    route_id: Optional[str] = None,
    vessel_class_id: Optional[int] = None,
    end_date: Optional[str] = None,
    cargo_id: Optional[int] = None,
) -> str:
    """Get market freight rates. start_date as YYYY-MM-DD (required).

    Use get_market_rate_routes to find available route IDs.
    cargo_id: 0=Dirty, 1=Clean, 2=IMO.
    """
    from signal_ocean.market_rates.enums import CargoId

    api = MarketRatesAPI(_connection())
    cid = CargoId(cargo_id) if cargo_id is not None else None
    return _serialize(
        api.get_market_rates(
            start_date=date.fromisoformat(start_date),
            route_id=route_id,
            vessel_class_id=vessel_class_id,
            end_date=_parse_date(end_date),
            cargo_id=cid,
        )
    )


@mcp.tool()
def get_market_rate_routes(
    vessel_class_id: Optional[int] = None,
) -> str:
    """Get available market rate routes, optionally filtered by vessel class."""
    api = MarketRatesAPI(_connection())
    return _serialize(api.get_routes(vessel_class_id=vessel_class_id))


# --- Freight Rates ---


@mcp.tool()
def get_freight_rates(
    load_ports: list[int],
    discharge_ports: list[int],
    vessel_classes: list[str],
    is_clean: bool,
    pricing_date: Optional[str] = None,
) -> str:
    """Get freight rates between ports for vessel classes.

    load_ports: List of load port IDs.
    discharge_ports: List of discharge port IDs.
    vessel_classes: List of vessel class names (e.g. ["VLCC", "Suezmax"]).
    is_clean: True for clean products, False for dirty.
    pricing_date: Date as YYYY-MM-DD (defaults to today).
    Use get_freight_rate_ports and get_freight_rate_vessel_classes for IDs.
    """
    api = FreightRatesAPI(_connection())
    d = date.fromisoformat(pricing_date) if pricing_date else date.today()
    return _serialize(
        api.get_freight_pricing(
            load_ports=load_ports,
            discharge_ports=discharge_ports,
            vessel_classes=vessel_classes,
            is_clean=is_clean,
            date=d,
        )
    )


@mcp.tool()
def get_freight_rate_vessel_classes() -> str:
    """Get available vessel class names for freight rate queries."""
    api = FreightRatesAPI(_connection())
    return json.dumps(list(api.get_vessel_classes()))


@mcp.tool()
def get_freight_rate_ports(name: Optional[str] = None) -> str:
    """Get available ports for freight rate queries."""
    from signal_ocean.freight_rates.port_filter import PortFilter

    api = FreightRatesAPI(_connection())
    pf = PortFilter(name_like=name) if name else None
    return _serialize(api.get_ports(port_filter=pf))


# --- Freight Pricing ---


@mcp.tool()
def get_freight_pricing(
    load_port_id: int,
    discharge_port_id: int,
    vessel_type_id: int,
    pricing_date: str,
) -> str:
    """Get freight pricing between ports for a vessel type.

    Use get_freight_pricing_ports and get_freight_pricing_vessel_types
    to find valid IDs. pricing_date as YYYY-MM-DD.
    """
    from signal_ocean.freight_pricing.port import Port
    from signal_ocean.freight_pricing.vessel_type import VesselType

    api = FreightPricingAPI(_connection())
    port_load = Port(id=load_port_id, name="")
    port_discharge = Port(id=discharge_port_id, name="")
    vtype = VesselType(id=vessel_type_id, name="")
    return _serialize(
        api.get_freight_pricing(
            vessel_type=vtype,
            load_port=port_load,
            discharge_port=port_discharge,
            date=date.fromisoformat(pricing_date),
        )
    )


@mcp.tool()
def get_freight_pricing_ports(name: Optional[str] = None) -> str:
    """Get available ports for freight pricing, optionally filtered by name."""
    from signal_ocean.freight_pricing.port_filter import PortFilter

    api = FreightPricingAPI(_connection())
    pf = PortFilter(name_like=name) if name else None
    return _serialize(api.get_ports(port_filter=pf))


@mcp.tool()
def get_freight_pricing_vessel_types() -> str:
    """Get available vessel types for freight pricing."""
    api = FreightPricingAPI(_connection())
    return _serialize(api.get_vessel_types())


# --- Distances ---


@mcp.tool()
def get_port_to_port_distance(
    vessel_class_id: int,
    loading_condition_id: int,
    port_from_id: int,
    port_to_id: int,
) -> str:
    """Get the sailing distance between two ports for a given vessel class.

    loading_condition_id: 0 = Laden, 1 = Ballast.
    Use get_distance_ports to find port IDs.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    api = DistancesAPI(_connection())
    vc = VesselClass(id=vessel_class_id, name="")
    pf = Port(id=port_from_id, name="")
    pt = Port(id=port_to_id, name="")
    result = api.get_port_to_port_distance(
        vessel_class=vc,
        loading_condition_id=loading_condition_id,
        port_from=pf,
        port_to=pt,
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
def get_port_to_port_route(
    vessel_class_id: int,
    loading_condition_id: int,
    port_from_id: int,
    port_to_id: int,
) -> str:
    """Get the sailing route between two ports for a given vessel class.

    Returns waypoints, distance, and route details.
    loading_condition_id: 0 = Laden, 1 = Ballast.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    api = DistancesAPI(_connection())
    vc = VesselClass(id=vessel_class_id, name="")
    pf = Port(id=port_from_id, name="")
    pt = Port(id=port_to_id, name="")
    return _serialize(
        api.get_port_to_port_route(
            vessel_class=vc,
            loading_condition_id=loading_condition_id,
            port_from=pf,
            port_to=pt,
        )
    )


@mcp.tool()
def get_point_to_point_distance(
    vessel_class_id: int,
    loading_condition_id: int,
    start_lon: float,
    start_lat: float,
    end_lon: float,
    end_lat: float,
) -> str:
    """Get the sailing distance between two coordinates.

    loading_condition_id: 0 = Laden, 1 = Ballast.
    Coordinates as decimal degrees (lon, lat).
    """
    from signal_ocean.distances.vessel_class import VesselClass
    from signal_ocean.distances.models import Point

    api = DistancesAPI(_connection())
    vc = VesselClass(id=vessel_class_id, name="")
    sp = Point(lon=start_lon, lat=start_lat)
    ep = Point(lon=end_lon, lat=end_lat)
    result = api.get_point_to_point_distance(
        vessel_class=vc,
        loading_condition_id=loading_condition_id,
        start_point=sp,
        end_point=ep,
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
def get_point_to_port_distance(
    vessel_class_id: int,
    loading_condition_id: int,
    point_lon: float,
    point_lat: float,
    port_id: int,
) -> str:
    """Get the sailing distance from a coordinate to a port.

    loading_condition_id: 0 = Laden, 1 = Ballast.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass
    from signal_ocean.distances.models import Point

    api = DistancesAPI(_connection())
    vc = VesselClass(id=vessel_class_id, name="")
    pt = Point(lon=point_lon, lat=point_lat)
    port = Port(id=port_id, name="")
    result = api.get_point_to_port_distance(
        vessel_class=vc,
        loading_condition_id=loading_condition_id,
        point=pt,
        port=port,
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
def get_generic_route(
    start_lon: float,
    start_lat: float,
    end_lon: float,
    end_lat: float,
    get_alternatives: Optional[bool] = None,
) -> str:
    """Get a generic sailing route between two coordinates.

    Not vessel-class specific. Returns waypoints and distance.
    """
    from signal_ocean.distances.models import Point

    api = DistancesAPI(_connection())
    sp = Point(lon=start_lon, lat=start_lat)
    ep = Point(lon=end_lon, lat=end_lat)
    return _serialize(
        api.get_generic_point_to_point_route(
            start_point=sp,
            end_point=ep,
            get_alternatives=get_alternatives,
        )
    )


@mcp.tool()
def get_distance_ports(name: Optional[str] = None) -> str:
    """Get available ports for distance calculations."""
    from signal_ocean.distances.port_filter import PortFilter

    api = DistancesAPI(_connection())
    pf = PortFilter(name_like=name) if name else None
    return _serialize(api.get_ports(port_filter=pf))


# --- Geos ---


@mcp.tool()
def get_ports_geo(port_id: Optional[int] = None) -> str:
    """Get port geographical data. Pass port_id for a specific port."""
    api = GeosAPI(_connection())
    return _serialize(api.get_ports(portId=port_id))


@mcp.tool()
def get_countries(country_id: Optional[int] = None) -> str:
    """Get country data. Pass country_id for a specific country."""
    api = GeosAPI(_connection())
    return _serialize(api.get_countries(countryId=country_id))


@mcp.tool()
def get_areas(area_id: Optional[int] = None) -> str:
    """Get maritime area data. Pass area_id for a specific area."""
    api = GeosAPI(_connection())
    return _serialize(api.get_areas(areaId=area_id))


@mcp.tool()
def get_geo_assets(geo_asset_id: Optional[int] = None) -> str:
    """Get geo asset data (terminals, refineries, storage facilities, etc.)."""
    api = GeosAPI(_connection())
    return _serialize(api.get_geoAssets(geoAssetId=geo_asset_id))


# --- Companies ---


@mcp.tool()
def get_company(company_id: int) -> str:
    """Get company details by ID."""
    api = CompaniesAPI(_connection())
    return _serialize(api.get_company(company_id))


@mcp.tool()
def search_companies(name: Optional[str] = None) -> str:
    """Search for companies by name."""
    api = CompaniesAPI(_connection())
    return _serialize(api.get_companies(name=name))


# --- Port Expenses ---


@mcp.tool()
def get_port_expenses(
    imo: int,
    port_id: int,
    vessel_type_id: Optional[int] = None,
) -> str:
    """Get estimated port expenses for a vessel at a specific port."""
    api = PortExpensesAPI(_connection())
    return _serialize(
        api.get_port_expenses(
            imo=imo, port_id=port_id, vessel_type_id=vessel_type_id
        )
    )


@mcp.tool()
def get_port_model_vessel_expenses(
    port_id: int,
    vessel_type_id: int,
    formula_calculation_date: str,
    vessel_class_id: int = 0,
    historical_tce: bool = False,
) -> str:
    """Get port expenses for a model vessel (not a specific IMO).

    formula_calculation_date as ISO datetime (YYYY-MM-DDTHH:MM:SS).
    """
    api = PortExpensesAPI(_connection())
    return _serialize(
        api.get_port_model_vessel_expenses(
            port_id=port_id,
            vessel_type_id=vessel_type_id,
            formula_calculation_date=datetime.fromisoformat(
                formula_calculation_date
            ),
            vessel_class_id=vessel_class_id,
            historical_tce=historical_tce,
        )
    )


@mcp.tool()
def get_port_expenses_required_params(
    port_id: int,
    vessel_type_id: int,
) -> str:
    """Get the required formula parameters for port expense calculation."""
    api = PortExpensesAPI(_connection())
    return json.dumps(
        api.get_required_formula_parameters(
            port_id=port_id, vessel_type_id=vessel_type_id
        )
    )


@mcp.tool()
def get_port_expenses_ports(name: Optional[str] = None) -> str:
    """Get available ports for port expense queries."""
    from signal_ocean.port_expenses.port_filter import PortFilter

    api = PortExpensesAPI(_connection())
    pf = PortFilter(name_like=name) if name else None
    return _serialize(api.get_ports(port_filter=pf))


@mcp.tool()
def get_port_expenses_vessel_types() -> str:
    """Get available vessel types for port expense queries."""
    api = PortExpensesAPI(_connection())
    return _serialize(api.get_vessel_types())


# --- Tonnage List ---


@mcp.tool()
def get_tonnage_list(
    loading_port_id: int,
    vessel_class_id: int,
    laycan_end_in_days: Optional[int] = None,
) -> str:
    """Get the current tonnage list for a loading port and vessel class.

    Shows available vessels near a port.
    Use get_tonnage_list_ports and get_vessel_classes to find IDs.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    api = TonnageListAPI(_connection())
    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    return _serialize(
        api.get_tonnage_list(
            loading_port=port,
            vessel_class=vc,
            laycan_end_in_days=laycan_end_in_days,
        )
    )


@mcp.tool()
def get_historical_tonnage_list(
    loading_port_id: int,
    vessel_class_id: int,
    laycan_end_in_days: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """Get historical tonnage list for a port and vessel class over a date range.

    Dates as YYYY-MM-DD.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    api = HistoricalTonnageListAPI(_connection())
    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    return _serialize(
        api.get_historical_tonnage_list(
            loading_port=port,
            vessel_class=vc,
            laycan_end_in_days=laycan_end_in_days,
            start_date=_parse_date(start_date),
            end_date=_parse_date(end_date),
        )
    )


@mcp.tool()
def get_tonnage_list_ports(name: Optional[str] = None) -> str:
    """Get available ports for tonnage list queries."""
    from signal_ocean.tonnage_list.models import PortFilter

    api = TonnageListAPI(_connection())
    pf = PortFilter(name_like=name) if name else None
    return _serialize(api.get_ports(port_filter=pf))


# --- Scraped Cargoes ---


@mcp.tool()
def get_scraped_cargoes(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
) -> str:
    """Get scraped cargo data from broker reports.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format (YYYY-MM-DDTHH:MM:SS).
    """
    api = ScrapedCargoesAPI(_connection())
    return _serialize(
        api.get_cargoes(
            vessel_type=vessel_type,
            received_date_from=_parse_datetime(received_date_from),
            received_date_to=_parse_datetime(received_date_to),
        )
    )


# --- Scraped Fixtures ---


@mcp.tool()
def get_scraped_fixtures(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped fixture data from broker reports.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format. Optionally filter by vessel IMO numbers.
    """
    api = ScrapedFixturesAPI(_connection())
    return _serialize(
        api.get_fixtures(
            vessel_type=vessel_type,
            received_date_from=_parse_datetime(received_date_from),
            received_date_to=_parse_datetime(received_date_to),
            imos=imos,
        )
    )


# --- Scraped Lineups ---


@mcp.tool()
def get_scraped_lineups(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped port lineup data.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    """
    api = ScrapedLineupsAPI(_connection())
    return _serialize(
        api.get_lineups(
            vessel_type=vessel_type,
            received_date_from=_parse_datetime(received_date_from),
            received_date_to=_parse_datetime(received_date_to),
            imos=imos,
        )
    )


# --- Scraped Positions ---


@mcp.tool()
def get_scraped_positions(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped vessel position data.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    """
    api = ScrapedPositionsAPI(_connection())
    return _serialize(
        api.get_positions(
            vessel_type=vessel_type,
            received_date_from=_parse_datetime(received_date_from),
            received_date_to=_parse_datetime(received_date_to),
            imos=imos,
        )
    )


def main() -> None:
    """Run the Signal Ocean MCP server."""
    mcp.run()
