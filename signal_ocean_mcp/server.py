"""Signal Ocean MCP Server.

Exposes Signal Ocean SDK APIs as MCP tools for use with
Claude and other MCP-compatible AI clients.
"""

import json
from contextlib import asynccontextmanager
from datetime import date, datetime
from functools import lru_cache
from typing import Any, List, Optional

import anyio
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

# --- Singleton API instances (one HTTP session for the server lifetime) ---
_conn: Connection
_companies_api: CompaniesAPI
_distances_api: DistancesAPI
_freight_pricing_api: FreightPricingAPI
_freight_rates_api: FreightRatesAPI
_geos_api: GeosAPI
_htl_api: HistoricalTonnageListAPI
_market_rates_api: MarketRatesAPI
_port_expenses_api: PortExpensesAPI
_tonnage_list_api: TonnageListAPI
_vessel_emissions_api: VesselEmissionsAPI
_vessel_valuations_api: VesselValuationsAPI
_vessels_api: VesselsAPI
_voyages_api: VoyagesAPI
_voyages_market_data_api: VoyagesMarketDataAPI
_scraped_cargoes_api: ScrapedCargoesAPI
_scraped_fixtures_api: ScrapedFixturesAPI
_scraped_lineups_api: ScrapedLineupsAPI
_scraped_positions_api: ScrapedPositionsAPI
_vessel_consumptions_api: VesselConsumptionsAPI


@asynccontextmanager
async def _lifespan(server: FastMCP):
    global _conn, _companies_api, _distances_api, _freight_pricing_api
    global _freight_rates_api, _geos_api, _htl_api, _market_rates_api
    global _port_expenses_api, _tonnage_list_api, _vessel_emissions_api
    global _vessel_valuations_api, _vessels_api, _voyages_api
    global _voyages_market_data_api, _scraped_cargoes_api, _scraped_fixtures_api
    global _scraped_lineups_api, _scraped_positions_api, _vessel_consumptions_api

    _conn = Connection()
    _companies_api = CompaniesAPI(_conn)
    _distances_api = DistancesAPI(_conn)
    _freight_pricing_api = FreightPricingAPI(_conn)
    _freight_rates_api = FreightRatesAPI(_conn)
    _geos_api = GeosAPI(_conn)
    _htl_api = HistoricalTonnageListAPI(_conn)
    _market_rates_api = MarketRatesAPI(_conn)
    _port_expenses_api = PortExpensesAPI(_conn)
    _tonnage_list_api = TonnageListAPI(_conn)
    _vessel_emissions_api = VesselEmissionsAPI(_conn)
    _vessel_valuations_api = VesselValuationsAPI(_conn)
    _vessels_api = VesselsAPI(_conn)
    _voyages_api = VoyagesAPI(_conn)
    _voyages_market_data_api = VoyagesMarketDataAPI(_conn)
    _scraped_cargoes_api = ScrapedCargoesAPI(_conn)
    _scraped_fixtures_api = ScrapedFixturesAPI(_conn)
    _scraped_lineups_api = ScrapedLineupsAPI(_conn)
    _scraped_positions_api = ScrapedPositionsAPI(_conn)
    _vessel_consumptions_api = VesselConsumptionsAPI(_conn)
    try:
        yield
    finally:
        _conn.close()


mcp = FastMCP(
    "Signal Ocean",
    lifespan=_lifespan,
    instructions=(
        "Signal Ocean provides maritime shipping data APIs. "
        "Use these tools to query vessel information, voyages, "
        "emissions, market rates, freight pricing, distances, "
        "port expenses, tonnage lists, and scraped market data. "
        "All tools require a valid Signal Ocean API key configured "
        "via the SIGNAL_OCEAN_API_KEY environment variable."
    ),
)


# --- Helpers ---

def _serialize(obj: Any) -> str:
    """Serialize SDK response objects to JSON strings."""
    if obj is None:
        return json.dumps(None)
    if isinstance(obj, (list, tuple)):
        return json.dumps([_to_dict(item) for item in obj], default=str)
    return json.dumps(_to_dict(obj), default=str)


def _to_dict(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", by_alias=True)
    if hasattr(obj, "__len__") and hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, dict)):
        items = list(obj)
        if items:
            return [_to_dict(item) for item in items]
        public = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        if public:
            return public
        return []
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    return obj


def _parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    return date.fromisoformat(value)


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value)


async def _resolve_port_by_name(get_ports_fn, port_name: str, registry: str):
    ports = list(await anyio.to_thread.run_sync(get_ports_fn) or [])
    if not ports:
        return None, f"No port found matching '{port_name}' in the {registry} registry"
    first = ports[0]
    pid = getattr(first, "id", None)
    if pid is None:
        d = _to_dict(first)
        pid = d.get("id") if isinstance(d, dict) else None
    return (pid, None) if pid else (None, f"Could not extract port ID for '{port_name}'")


async def _resolve_distances_port(port_id: Optional[int], port_name: Optional[str]):
    if port_id is not None:
        return port_id, None
    if not port_name:
        return None, "Provide port_id or port_name"
    from signal_ocean.distances.port_filter import PortFilter
    return await _resolve_port_by_name(
        lambda: _distances_api.get_ports(port_filter=PortFilter(name_like=port_name)),
        port_name, "distances",
    )


async def _resolve_freight_rate_port(port_id: Optional[int], port_name: Optional[str]):
    if port_id is not None:
        return port_id, None
    if not port_name:
        return None, "Provide port_id or port_name"
    from signal_ocean.freight_rates.port_filter import PortFilter
    return await _resolve_port_by_name(
        lambda: _freight_rates_api.get_ports(port_filter=PortFilter(name_like=port_name)),
        port_name, "freight_rates",
    )


async def _resolve_freight_pricing_port(port_id: Optional[int], port_name: Optional[str]):
    if port_id is not None:
        return port_id, None
    if not port_name:
        return None, "Provide port_id or port_name"
    from signal_ocean.freight_pricing.port_filter import PortFilter
    return await _resolve_port_by_name(
        lambda: _freight_pricing_api.get_ports(port_filter=PortFilter(name_like=port_name)),
        port_name, "freight_pricing",
    )


async def _resolve_port_expenses_port(port_id: Optional[int], port_name: Optional[str]):
    if port_id is not None:
        return port_id, None
    if not port_name:
        return None, "Provide port_id or port_name"
    from signal_ocean.port_expenses.port_filter import PortFilter
    return await _resolve_port_by_name(
        lambda: _port_expenses_api.get_ports(port_filter=PortFilter(name_like=port_name)),
        port_name, "port_expenses",
    )


async def _resolve_tonnage_list_port(port_id: Optional[int], port_name: Optional[str]):
    if port_id is not None:
        return port_id, None
    if not port_name:
        return None, "Provide loading_port_id or loading_port_name"
    from signal_ocean.tonnage_list.models import PortFilter
    return await _resolve_port_by_name(
        lambda: _tonnage_list_api.get_ports(port_filter=PortFilter(name_like=port_name)),
        port_name, "tonnage_list",
    )


# --- Cached reference data (static lookups, fetched once per process) ---

@lru_cache(maxsize=None)
def _vessel_classes_sync():
    return _vessels_api.get_vessel_classes()


@lru_cache(maxsize=None)
def _vessel_types_sync():
    return _vessels_api.get_vessel_types()


@lru_cache(maxsize=None)
def _market_rate_routes_sync(vessel_class_id: Optional[int]):
    return _market_rates_api.get_routes(vessel_class_id=vessel_class_id)


@lru_cache(maxsize=None)
def _freight_rate_vessel_classes_sync():
    return list(_freight_rates_api.get_vessel_classes())


@lru_cache(maxsize=None)
def _freight_pricing_vessel_types_sync():
    return _freight_pricing_api.get_vessel_types()


@lru_cache(maxsize=None)
def _port_expenses_vessel_types_sync():
    return _port_expenses_api.get_vessel_types()


@lru_cache(maxsize=None)
def _countries_sync(country_id: Optional[int]):
    return _geos_api.get_countries(countryId=country_id)


# --- Vessel Lookup ---


@mcp.tool()
async def search_vessel_imos(name: Optional[str] = None) -> str:
    """Search for vessel IMO numbers by name.

    Returns vessels with their IMO and name. Use this to find
    a vessel's IMO before querying voyages or other APIs.
    """
    from signal_ocean.voyages.models import VesselFilter

    vf = VesselFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _voyages_api.get_imos(vf))
    )


# --- Vessels ---


@mcp.tool()
async def get_vessel(imo: int) -> str:
    """Get detailed information about a specific vessel by its IMO number."""
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _vessels_api.get_vessel(imo))
    )


@mcp.tool()
async def search_vessels(name: Optional[str] = None) -> str:
    """Search for vessels by name. Returns all vessels if no name given."""
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _vessels_api.get_vessels(name=name))
    )


@mcp.tool()
async def get_vessels_by_vessel_class(vessel_class_id: int) -> str:
    """Get all vessels belonging to a specific vessel class.

    Use get_vessel_classes to find available vessel class IDs.
    """
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessels_api.get_vessels_by_vessel_class(vesselClass=vessel_class_id)
        )
    )


@mcp.tool()
async def get_vessel_classes() -> str:
    """Get all available vessel classes with their IDs.

    Common tanker classes: VLCC, Suezmax, Aframax, LR2, LR1, MR2, MR1, SR, GP.
    Common dry bulk classes: Capesize, Kamsarmax, Panamax, Ultramax, Supramax,
    Handymax, Handysize, VLOC.
    Other: LPG, LNG, Container.
    Call this once to resolve a class name to an ID for use in other tools.
    """
    return _serialize(await anyio.to_thread.run_sync(_vessel_classes_sync))


@mcp.tool()
async def get_vessel_types() -> str:
    """Get all available vessel types with their IDs.

    Known types: Tanker (1), Dry Bulk (3), LPG (6), LNG (4), Container (5).
    Type IDs are used in scraped data tools (vessel_type param) and voyage filters.
    """
    return _serialize(await anyio.to_thread.run_sync(_vessel_types_sync))


@mcp.tool()
async def get_vessel_name_history(imo: int) -> str:
    """Get the name history for a vessel by IMO number."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessels_api.get_vessels_name_history(imo=imo)
        )
    )


@mcp.tool()
async def get_vessel_commercial_operator_history(imo: int) -> str:
    """Get the commercial operator history for a vessel by IMO number."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessels_api.get_vessels_commOp_history(imo=imo)
        )
    )


@mcp.tool()
async def get_vessel_flag_history(imo: int) -> str:
    """Get the flag (country of registration) history for a vessel by IMO."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessels_api.get_vessels_flag_history(imo=imo)
        )
    )


# --- Vessel Emissions ---


@mcp.tool()
async def get_vessel_emissions(
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
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_emissions_by_imo(
                imo,
                include_consumptions=include_consumptions,
                include_efficiency_metrics=include_efficiency_metrics,
                include_distances=include_distances,
                include_durations=include_durations,
                include_eu_emissions=include_eu_emissions,
            )
        )
    )


@mcp.tool()
async def get_voyage_emissions(
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
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_emissions_by_imo_and_voyage_number(
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
    )


@mcp.tool()
async def get_vessel_class_emissions(
    vessel_class_id: int,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = False,
    include_distances: bool = False,
    include_durations: bool = False,
    include_speed_statistics: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions data for all vessels in a vessel class."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_emissions_by_vessel_class_id(
                vessel_class_id=vessel_class_id,
                include_consumptions=include_consumptions,
                include_efficiency_metrics=include_efficiency_metrics,
                include_distances=include_distances,
                include_durations=include_durations,
                include_speed_statistics=include_speed_statistics,
                include_eu_emissions=include_eu_emissions,
            )
        )
    )


@mcp.tool()
async def get_vessel_emission_metrics(
    imo: int, year: Optional[int] = None
) -> str:
    """Get emission metrics (CII, AER, EEOI) for a vessel by IMO."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_metrics_by_imo(imo, year=year)
        )
    )


@mcp.tool()
async def get_vessel_class_emission_metrics(
    vessel_class_id: int, year: Optional[int] = None
) -> str:
    """Get emission metrics (CII, AER, EEOI) for all vessels in a class."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_metrics_by_vessel_class_id(
                vessel_class_id=vessel_class_id, year=year
            )
        )
    )


# --- Vessel Consumptions ---


@mcp.tool()
async def get_vessel_consumptions(imo: int) -> str:
    """Get fuel consumption data for a vessel by IMO number."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_consumptions_api.get_consumptions(imo)
        )
    )


@mcp.tool()
async def get_vessel_advertised_consumptions(imo: int) -> str:
    """Get advertised (reported) fuel consumption data for a vessel."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_consumptions_api.get_advertised_consumptions(imo)
        )
    )


# --- Vessel Valuations ---


@mcp.tool()
async def get_vessel_valuation(imo: int) -> str:
    """Get the latest valuation for a vessel by IMO number."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_valuations_api.get_latest_valuation_by_imo(imo)
        )
    )


@mcp.tool()
async def get_vessel_historical_valuations(
    imo: int,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    """Get historical valuations for a vessel. Dates as YYYY-MM-DD."""
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_valuations_api.get_all_historical_valuations_by_imo(
                imo, from_date=from_date, to_date=to_date
            )
        )
    )


@mcp.tool()
async def get_vessel_valuations_for_list(imo_list: list[int]) -> str:
    """Get latest valuations for multiple vessels at once.

    Pass a list of IMO numbers.
    """
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_valuations_api.get_latest_valuations_for_list_of_vessels(
                imo_list
            )
        )
    )


@mcp.tool()
async def get_vessel_valuations_paged(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    changed_since: Optional[str] = None,
) -> str:
    """Get latest valuations for all vessels, paginated.

    changed_since as YYYY-MM-DD to get only recently updated valuations.
    """
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _vessel_valuations_api.get_latest_valuations_by_page(
                page=page, page_size=page_size, changed_since=changed_since
            )
        )
    )


# --- Voyages ---


@mcp.tool()
async def get_voyages(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyage data for vessels.

    Filter by IMO, vessel class ID, vessel type ID, or start date
    (YYYY-MM-DD). At least one filter is recommended to limit results.
    """
    d = _parse_date(date_from)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_api.get_voyages(
                imo=imo,
                vessel_class_id=vessel_class_id,
                vessel_type_id=vessel_type_id,
                date_from=d,
            )
        )
    )


@mcp.tool()
async def get_voyages_condensed(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get condensed voyage data (lighter payload than full voyages)."""
    d = _parse_date(date_from)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_api.get_voyages_condensed(
                imo=imo,
                vessel_class_id=vessel_class_id,
                vessel_type_id=vessel_type_id,
                date_from=d,
            )
        )
    )


@mcp.tool()
async def get_voyages_flat(
    imo: Optional[int] = None,
    vessel_class_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyages in flat format (separate lists for voyages, events, details, geos).

    Useful for large datasets as it avoids deeply nested structures.
    """
    d = _parse_date(date_from)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_api.get_voyages_flat(
                imo=imo,
                vessel_class_id=vessel_class_id,
                vessel_type_id=vessel_type_id,
                date_from=d,
            )
        )
    )


@mcp.tool()
async def get_voyages_advanced_search(
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
    sdf = _parse_date(start_date_from)
    sdt = _parse_date(start_date_to)
    fldf = _parse_date(first_load_arrival_date_from)
    fldt = _parse_date(first_load_arrival_date_to)
    edf = _parse_date(end_date_from)
    edt = _parse_date(end_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_api.get_voyages_by_advanced_search(
                imos=imos,
                vessel_class_id=vessel_class_id,
                vessel_class_ids=vessel_class_ids,
                vessel_type_id=vessel_type_id,
                port_id=port_id,
                port_ids=port_ids,
                commercial_operator_id=commercial_operator_id,
                charterer_id=charterer_id,
                start_date_from=sdf,
                start_date_to=sdt,
                first_load_arrival_date_from=fldf,
                first_load_arrival_date_to=fldt,
                end_date_from=edf,
                end_date_to=edt,
                event_type=event_type,
                event_purpose=event_purpose,
                event_horizon=event_horizon,
                voyage_horizon=voyage_horizon,
                hide_event_details=hide_event_details,
                hide_events=hide_events,
                hide_market_info=hide_market_info,
            )
        )
    )


# --- Voyages Market Data ---


@mcp.tool()
async def get_voyage_market_data(
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
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_market_data_api.get_voyage_market_data(
                imo=imo,
                vessel_class_id=vessel_class_id,
                vessel_type_id=vessel_type_id,
                include_vessel_details=include_vessel_details,
                include_fixtures=include_fixtures,
                include_matched_fixture=include_matched_fixture,
                include_labels=include_labels,
            )
        )
    )


@mcp.tool()
async def get_voyage_market_data_advanced(
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
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _voyages_market_data_api.get_voyage_market_data_advanced(
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
    )


# --- Market Rates ---


@mcp.tool()
async def get_market_rates(
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

    sd = date.fromisoformat(start_date)
    ed = _parse_date(end_date)
    cid = CargoId(cargo_id) if cargo_id is not None else None
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _market_rates_api.get_market_rates(
                start_date=sd,
                route_id=route_id,
                vessel_class_id=vessel_class_id,
                end_date=ed,
                cargo_id=cid,
            )
        )
    )


@mcp.tool()
async def get_market_rate_routes(
    vessel_class_id: Optional[int] = None,
) -> str:
    """Get available market rate routes, optionally filtered by vessel class.

    Route names follow Signal Ocean conventions (e.g. 'MR2 - Cont/USAC',
    'VLCC - MEG/China') rather than standard industry codes (TC2, TD3C).
    Call this first to discover exact route names and IDs, then pass them
    to get_market_rates_by_route_name or get_market_rates.
    Use get_vessel_classes to find vessel_class_id values.
    """
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _market_rate_routes_sync(vessel_class_id)
        )
    )


# --- Freight Rates ---


@mcp.tool()
async def get_freight_rates(
    vessel_classes: list[str],
    is_clean: bool,
    load_ports: Optional[list[int]] = None,
    discharge_ports: Optional[list[int]] = None,
    load_port_name: Optional[str] = None,
    discharge_port_name: Optional[str] = None,
    pricing_date: Optional[str] = None,
) -> str:
    """Get freight rates between ports for vessel classes.

    vessel_classes: List of vessel class names (e.g. ["VLCC", "Suezmax"]).
    is_clean: True for clean products, False for dirty.
    Provide port IDs (load_ports/discharge_ports) or port names
    (load_port_name/discharge_port_name) — names are resolved automatically.
    pricing_date: YYYY-MM-DD (defaults to today).
    """
    resolved_load = list(load_ports or [])
    if load_port_name:
        pid, err = await _resolve_freight_rate_port(None, load_port_name)
        if err:
            return json.dumps({"error": err})
        resolved_load.append(pid)
    if not resolved_load:
        return json.dumps({"error": "Provide load_ports or load_port_name"})

    resolved_discharge = list(discharge_ports or [])
    if discharge_port_name:
        pid, err = await _resolve_freight_rate_port(None, discharge_port_name)
        if err:
            return json.dumps({"error": err})
        resolved_discharge.append(pid)
    if not resolved_discharge:
        return json.dumps({"error": "Provide discharge_ports or discharge_port_name"})

    d = date.fromisoformat(pricing_date) if pricing_date else date.today()
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _freight_rates_api.get_freight_pricing(
                load_ports=resolved_load,
                discharge_ports=resolved_discharge,
                vessel_classes=vessel_classes,
                is_clean=is_clean,
                date=d,
            )
        )
    )


@mcp.tool()
async def get_freight_rate_vessel_classes() -> str:
    """Get available vessel class names for freight rate queries."""
    result = await anyio.to_thread.run_sync(_freight_rate_vessel_classes_sync)
    return json.dumps(result)


@mcp.tool()
async def get_freight_rate_ports(name: Optional[str] = None) -> str:
    """Get available ports for freight rate queries."""
    from signal_ocean.freight_rates.port_filter import PortFilter

    pf = PortFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _freight_rates_api.get_ports(port_filter=pf))
    )


# --- Freight Pricing ---


@mcp.tool()
async def get_freight_pricing(
    vessel_type_id: int,
    pricing_date: str,
    load_port_id: Optional[int] = None,
    discharge_port_id: Optional[int] = None,
    load_port_name: Optional[str] = None,
    discharge_port_name: Optional[str] = None,
) -> str:
    """Get freight pricing between ports for a vessel type.

    Use get_freight_pricing_vessel_types to find vessel_type_id.
    Provide port IDs or port names — names are resolved automatically.
    pricing_date as YYYY-MM-DD.
    """
    from signal_ocean.freight_pricing.port import Port
    from signal_ocean.freight_pricing.vessel_type import VesselType

    load_port_id, err = await _resolve_freight_pricing_port(load_port_id, load_port_name)
    if err:
        return json.dumps({"error": err})
    discharge_port_id, err = await _resolve_freight_pricing_port(discharge_port_id, discharge_port_name)
    if err:
        return json.dumps({"error": err})

    port_load = Port(id=load_port_id, name="")
    port_discharge = Port(id=discharge_port_id, name="")
    vtype = VesselType(id=vessel_type_id, name="")
    d = date.fromisoformat(pricing_date)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _freight_pricing_api.get_freight_pricing(
                vessel_type=vtype,
                load_port=port_load,
                discharge_port=port_discharge,
                date=d,
            )
        )
    )


@mcp.tool()
async def get_freight_pricing_ports(name: Optional[str] = None) -> str:
    """Get available ports for freight pricing, optionally filtered by name."""
    from signal_ocean.freight_pricing.port_filter import PortFilter

    pf = PortFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _freight_pricing_api.get_ports(port_filter=pf)
        )
    )


@mcp.tool()
async def get_freight_pricing_vessel_types() -> str:
    """Get available vessel types for freight pricing."""
    return _serialize(
        await anyio.to_thread.run_sync(_freight_pricing_vessel_types_sync)
    )


# --- Distances ---


@mcp.tool()
async def get_port_to_port_distance(
    vessel_class_id: int,
    loading_condition_id: int,
    port_from_id: Optional[int] = None,
    port_to_id: Optional[int] = None,
    port_from_name: Optional[str] = None,
    port_to_name: Optional[str] = None,
) -> str:
    """Get the sailing distance between two ports for a given vessel class.

    loading_condition_id: 0 = Laden, 1 = Ballast.
    Provide port IDs or port names — names are resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    port_from_id, err = await _resolve_distances_port(port_from_id, port_from_name)
    if err:
        return json.dumps({"error": err})
    port_to_id, err = await _resolve_distances_port(port_to_id, port_to_name)
    if err:
        return json.dumps({"error": err})

    vc = VesselClass(id=vessel_class_id, name="")
    pf = Port(id=port_from_id, name="")
    pt = Port(id=port_to_id, name="")
    result = await anyio.to_thread.run_sync(
        lambda: _distances_api.get_port_to_port_distance(
            vessel_class=vc,
            loading_condition_id=loading_condition_id,
            port_from=pf,
            port_to=pt,
        )
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
async def get_port_to_port_route(
    vessel_class_id: int,
    loading_condition_id: int,
    port_from_id: Optional[int] = None,
    port_to_id: Optional[int] = None,
    port_from_name: Optional[str] = None,
    port_to_name: Optional[str] = None,
) -> str:
    """Get the sailing route between two ports for a given vessel class.

    Returns waypoints, distance, and route details.
    loading_condition_id: 0 = Laden, 1 = Ballast.
    Provide port IDs or port names — names are resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    port_from_id, err = await _resolve_distances_port(port_from_id, port_from_name)
    if err:
        return json.dumps({"error": err})
    port_to_id, err = await _resolve_distances_port(port_to_id, port_to_name)
    if err:
        return json.dumps({"error": err})

    vc = VesselClass(id=vessel_class_id, name="")
    pf = Port(id=port_from_id, name="")
    pt = Port(id=port_to_id, name="")
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _distances_api.get_port_to_port_route(
                vessel_class=vc,
                loading_condition_id=loading_condition_id,
                port_from=pf,
                port_to=pt,
            )
        )
    )


@mcp.tool()
async def get_point_to_point_distance(
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

    vc = VesselClass(id=vessel_class_id, name="")
    sp = Point(lon=start_lon, lat=start_lat)
    ep = Point(lon=end_lon, lat=end_lat)
    result = await anyio.to_thread.run_sync(
        lambda: _distances_api.get_point_to_point_distance(
            vessel_class=vc,
            loading_condition_id=loading_condition_id,
            start_point=sp,
            end_point=ep,
        )
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
async def get_point_to_port_distance(
    vessel_class_id: int,
    loading_condition_id: int,
    point_lon: float,
    point_lat: float,
    port_id: Optional[int] = None,
    port_name: Optional[str] = None,
) -> str:
    """Get the sailing distance from a coordinate to a port.

    loading_condition_id: 0 = Laden, 1 = Ballast.
    Provide port_id or port_name — name is resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass
    from signal_ocean.distances.models import Point

    port_id, err = await _resolve_distances_port(port_id, port_name)
    if err:
        return json.dumps({"error": err})

    vc = VesselClass(id=vessel_class_id, name="")
    pt = Point(lon=point_lon, lat=point_lat)
    port = Port(id=port_id, name="")
    result = await anyio.to_thread.run_sync(
        lambda: _distances_api.get_point_to_port_distance(
            vessel_class=vc,
            loading_condition_id=loading_condition_id,
            point=pt,
            port=port,
        )
    )
    return json.dumps({"distance_nm": float(result) if result else None})


@mcp.tool()
async def get_generic_route(
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

    sp = Point(lon=start_lon, lat=start_lat)
    ep = Point(lon=end_lon, lat=end_lat)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _distances_api.get_generic_point_to_point_route(
                start_point=sp,
                end_point=ep,
                get_alternatives=get_alternatives,
            )
        )
    )


@mcp.tool()
async def get_distance_ports(name: Optional[str] = None) -> str:
    """Get available ports for distance calculations."""
    from signal_ocean.distances.port_filter import PortFilter

    pf = PortFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _distances_api.get_ports(port_filter=pf))
    )


# --- Geos ---


@mcp.tool()
async def get_ports_geo(port_id: Optional[int] = None) -> str:
    """Get port geographical data. Pass port_id for a specific port.

    Requires Geos API subscription. Returns 401 Unauthorized if the
    configured API key does not have access to this endpoint.
    """
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _geos_api.get_ports(portId=port_id))
    )


@mcp.tool()
async def get_countries(country_id: Optional[int] = None) -> str:
    """Get country data. Pass country_id for a specific country.

    Requires Geos API subscription. Returns 401 Unauthorized if the
    configured API key does not have access to this endpoint.
    """
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _countries_sync(country_id))
    )


@mcp.tool()
async def get_areas(area_id: Optional[int] = None) -> str:
    """Get maritime area data. Pass area_id for a specific area.

    Requires Geos API subscription. Returns 401 Unauthorized if the
    configured API key does not have access to this endpoint.
    """
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _geos_api.get_areas(areaId=area_id))
    )


@mcp.tool()
async def get_geo_assets(geo_asset_id: Optional[int] = None) -> str:
    """Get geo asset data (terminals, refineries, storage facilities, etc.).

    Requires Geos API subscription. Returns 401 Unauthorized if the
    configured API key does not have access to this endpoint.
    """
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _geos_api.get_geoAssets(geoAssetId=geo_asset_id)
        )
    )


# --- Companies ---


@mcp.tool()
async def get_company(company_id: int) -> str:
    """Get company details by ID."""
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _companies_api.get_company(company_id))
    )


@mcp.tool()
async def search_companies(name: Optional[str] = None) -> str:
    """Search for companies by name."""
    return _serialize(
        await anyio.to_thread.run_sync(lambda: _companies_api.get_companies(name=name))
    )


# --- Port Expenses ---


@mcp.tool()
async def get_port_expenses(
    imo: int,
    port_id: Optional[int] = None,
    vessel_type_id: Optional[int] = None,
    port_name: Optional[str] = None,
) -> str:
    """Get estimated port expenses for a vessel at a specific port.

    Provide port_id or port_name — name is resolved automatically.
    """
    port_id, err = await _resolve_port_expenses_port(port_id, port_name)
    if err:
        return json.dumps({"error": err})
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _port_expenses_api.get_port_expenses(
                imo=imo, port_id=port_id, vessel_type_id=vessel_type_id
            )
        )
    )


@mcp.tool()
async def get_port_model_vessel_expenses(
    vessel_type_id: int,
    formula_calculation_date: str,
    port_id: Optional[int] = None,
    port_name: Optional[str] = None,
    vessel_class_id: int = 0,
    historical_tce: bool = False,
) -> str:
    """Get port expenses for a model vessel (not a specific IMO).

    formula_calculation_date as ISO datetime (YYYY-MM-DDTHH:MM:SS).
    Provide port_id or port_name — name is resolved automatically.
    """
    port_id, err = await _resolve_port_expenses_port(port_id, port_name)
    if err:
        return json.dumps({"error": err})
    dt = datetime.fromisoformat(formula_calculation_date)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _port_expenses_api.get_port_model_vessel_expenses(
                port_id=port_id,
                vessel_type_id=vessel_type_id,
                formula_calculation_date=dt,
                vessel_class_id=vessel_class_id,
                historical_tce=historical_tce,
            )
        )
    )


@mcp.tool()
async def get_port_expenses_required_params(
    vessel_type_id: int,
    port_id: Optional[int] = None,
    port_name: Optional[str] = None,
) -> str:
    """Get the required formula parameters for port expense calculation.

    Provide port_id or port_name — name is resolved automatically.
    """
    port_id, err = await _resolve_port_expenses_port(port_id, port_name)
    if err:
        return json.dumps({"error": err})
    result = await anyio.to_thread.run_sync(
        lambda: _port_expenses_api.get_required_formula_parameters(
            port_id=port_id, vessel_type_id=vessel_type_id
        )
    )
    return json.dumps(result)


@mcp.tool()
async def get_port_expenses_ports(name: Optional[str] = None) -> str:
    """Get available ports for port expense queries."""
    from signal_ocean.port_expenses.port_filter import PortFilter

    pf = PortFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _port_expenses_api.get_ports(port_filter=pf)
        )
    )


@mcp.tool()
async def get_port_expenses_vessel_types() -> str:
    """Get available vessel types for port expense queries."""
    return _serialize(
        await anyio.to_thread.run_sync(_port_expenses_vessel_types_sync)
    )


# --- Tonnage List ---


@mcp.tool()
async def get_tonnage_list(
    vessel_class_id: int,
    loading_port_id: Optional[int] = None,
    loading_port_name: Optional[str] = None,
    laycan_end_in_days: Optional[int] = None,
) -> str:
    """Get the current tonnage list for a loading port and vessel class.

    Shows available vessels near a port.
    Provide loading_port_id or loading_port_name — name is resolved automatically.
    Use get_vessel_classes to find vessel_class_id.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    loading_port_id, err = await _resolve_tonnage_list_port(loading_port_id, loading_port_name)
    if err:
        return json.dumps({"error": err})

    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _tonnage_list_api.get_tonnage_list(
                loading_port=port,
                vessel_class=vc,
                laycan_end_in_days=laycan_end_in_days,
            )
        )
    )


@mcp.tool()
async def get_historical_tonnage_list(
    vessel_class_id: int,
    loading_port_id: Optional[int] = None,
    loading_port_name: Optional[str] = None,
    laycan_end_in_days: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """Get historical tonnage list for a port and vessel class over a date range.

    Dates as YYYY-MM-DD.
    Provide loading_port_id or loading_port_name — name is resolved automatically.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    loading_port_id, err = await _resolve_tonnage_list_port(loading_port_id, loading_port_name)
    if err:
        return json.dumps({"error": err})

    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _htl_api.get_historical_tonnage_list(
                loading_port=port,
                vessel_class=vc,
                laycan_end_in_days=laycan_end_in_days,
                start_date=sd,
                end_date=ed,
            )
        )
    )


@mcp.tool()
async def get_tonnage_list_ports(name: Optional[str] = None) -> str:
    """Get available ports for tonnage list queries."""
    from signal_ocean.tonnage_list.models import PortFilter

    pf = PortFilter(name_like=name) if name else None
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _tonnage_list_api.get_ports(port_filter=pf)
        )
    )


# --- Scraped Cargoes ---


@mcp.tool()
async def get_scraped_cargoes(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
) -> str:
    """Get scraped cargo data from broker reports.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format (YYYY-MM-DDTHH:MM:SS).
    """
    df = _parse_datetime(received_date_from)
    dt = _parse_datetime(received_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _scraped_cargoes_api.get_cargoes(
                vessel_type=vessel_type,
                received_date_from=df,
                received_date_to=dt,
            )
        )
    )


# --- Scraped Fixtures ---


@mcp.tool()
async def get_scraped_fixtures(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped fixture data from broker reports.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format. Optionally filter by vessel IMO numbers.
    """
    df = _parse_datetime(received_date_from)
    dt = _parse_datetime(received_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _scraped_fixtures_api.get_fixtures(
                vessel_type=vessel_type,
                received_date_from=df,
                received_date_to=dt,
                imos=imos,
            )
        )
    )


# --- Scraped Lineups ---


@mcp.tool()
async def get_scraped_lineups(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped port lineup data.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    """
    df = _parse_datetime(received_date_from)
    dt = _parse_datetime(received_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _scraped_lineups_api.get_lineups(
                vessel_type=vessel_type,
                received_date_from=df,
                received_date_to=dt,
                imos=imos,
            )
        )
    )


# --- Scraped Positions ---


@mcp.tool()
async def get_scraped_positions(
    vessel_type: int,
    received_date_from: Optional[str] = None,
    received_date_to: Optional[str] = None,
    imos: Optional[list[int]] = None,
) -> str:
    """Get scraped vessel position data.

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    """
    df = _parse_datetime(received_date_from)
    dt = _parse_datetime(received_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _scraped_positions_api.get_positions(
                vessel_type=vessel_type,
                received_date_from=df,
                received_date_to=dt,
                imos=imos,
            )
        )
    )


# --- Composite Tools (collapse common multi-call patterns into single tool calls) ---


def _aggregate_class_metrics(metrics_iterable) -> dict:
    """Compute summary stats over per-vessel class emission metrics."""
    if metrics_iterable is None:
        return {}
    items = list(metrics_iterable)
    if not items:
        return {"vessel_count": 0}

    cii_scores: list[float] = []
    rating_dist: dict[str, int] = {}
    for m in items:
        d = _to_dict(m)
        if not isinstance(d, dict):
            continue
        score = d.get("cii_score") or d.get("ciiScore")
        if score is not None:
            try:
                cii_scores.append(float(score))
            except (ValueError, TypeError):
                pass
        rating = d.get("cii_rating") or d.get("ciiRating")
        if rating:
            key = str(rating)
            rating_dist[key] = rating_dist.get(key, 0) + 1

    summary: dict = {"vessel_count": len(items), "cii_rating_distribution": rating_dist}
    if cii_scores:
        cii_scores.sort()
        n = len(cii_scores)
        summary["cii_score_stats"] = {
            "mean": round(sum(cii_scores) / n, 4),
            "median": cii_scores[n // 2],
            "p25": cii_scores[n // 4],
            "p75": cii_scores[3 * n // 4],
            "min": cii_scores[0],
            "max": cii_scores[-1],
        }
    return summary


def _pick_latest_completed(voyages_iterable) -> Any:
    """Return the most recent completed voyage from an iterable."""
    items = list(voyages_iterable)
    if not items:
        return None
    completed = [
        v for v in items
        if getattr(v, "end_date", None) is not None
        and getattr(v, "voyage_horizon", None) in ("Historical", "historical", None)
    ]
    if not completed:
        completed = [
            v for v in items
            if getattr(v, "voyage_horizon", None) in ("Historical", "historical")
        ]
    if not completed:
        completed = items
    return max(completed, key=lambda v: str(getattr(v, "start_date", "") or ""), default=None)


@mcp.tool()
async def get_vessel_by_name(name: str) -> str:
    """Find a vessel by name and return its full details in one call.

    Combines search_vessels + get_vessel. Returns the closest name match
    including vessel class, type, DWT, and build year.
    Use this instead of calling search_vessels followed by get_vessel.
    """
    vessels = await anyio.to_thread.run_sync(lambda: _vessels_api.get_vessels(name=name))
    if not vessels:
        return json.dumps({"error": f"No vessel found matching '{name}'"})
    imo = vessels[0].imo
    vessel = await anyio.to_thread.run_sync(lambda: _vessels_api.get_vessel(imo))
    return _serialize(vessel)


@mcp.tool()
async def get_latest_completed_voyage(imo: int) -> str:
    """Get the most recently completed voyage for a vessel in one call.

    Combines get_voyages_condensed + filtering. Returns a single voyage
    with start/end dates, load/discharge ports, and cargo info.
    Use this instead of fetching all voyages and filtering client-side.
    """
    voyages = await anyio.to_thread.run_sync(
        lambda: _voyages_api.get_voyages_condensed(imo=imo)
    )
    if not voyages:
        return json.dumps({"error": f"No voyages found for IMO {imo}"})
    latest = _pick_latest_completed(voyages)
    return _serialize(latest)


@mcp.tool()
async def get_latest_voyage_emissions(
    imo: int,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = True,
    include_distances: bool = False,
    include_durations: bool = False,
    include_speed_statistics: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions for a vessel's most recently completed voyage in one call.

    Combines get_voyages_condensed + get_voyage_emissions. Eliminates the
    two-step lookup (list voyages → extract voyage_number → fetch emissions).
    Returns voyage metadata alongside emission data.
    include_efficiency_metrics defaults to True (CII, AER, EEOI included).
    """
    voyages = await anyio.to_thread.run_sync(
        lambda: _voyages_api.get_voyages_condensed(imo=imo)
    )
    if not voyages:
        return json.dumps({"error": f"No voyages found for IMO {imo}"})

    latest = _pick_latest_completed(voyages)
    if latest is None:
        return json.dumps({"error": "No completed voyage found"})

    voyage_number = getattr(latest, "voyage_number", None)
    if voyage_number is None:
        return json.dumps({"error": "Could not determine voyage_number from voyage data"})

    emissions = await anyio.to_thread.run_sync(
        lambda: _vessel_emissions_api.get_emissions_by_imo_and_voyage_number(
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
    return json.dumps(
        {"voyage": _to_dict(latest), "emissions": _to_dict(emissions)},
        default=str,
    )


@mcp.tool()
async def get_vessel_emission_benchmark(imo: int, year: Optional[int] = None) -> str:
    """Compare a vessel's emission metrics against its peer class distribution.

    Combines get_vessel + get_vessel_emission_metrics + get_vessel_class_emission_metrics
    into one call. Returns the vessel's CII/AER/EEOI alongside class-level
    summary stats (mean, median, p25/p75, rating distribution) instead of
    the raw 500-record class payload. Eliminates the 5-call chain required
    to answer a benchmark question.
    year should be a completed calendar year (e.g. 2024, 2025); passing the
    current year returns partial data. Omit to get the SDK default.
    """
    vessel = await anyio.to_thread.run_sync(lambda: _vessels_api.get_vessel(imo))
    if vessel is None:
        return json.dumps({"error": f"Vessel with IMO {imo} not found"})

    vd = _to_dict(vessel)
    vessel_class_id = vd.get("vessel_class_id") or vd.get("vesselClassId")
    vessel_class_name = vd.get("vessel_class") or vd.get("vesselClass")

    vessel_metrics = await anyio.to_thread.run_sync(
        lambda: _vessel_emissions_api.get_metrics_by_imo(imo, year=year)
    )

    class_summary: dict = {}
    if vessel_class_id is not None:
        class_metrics = await anyio.to_thread.run_sync(
            lambda: _vessel_emissions_api.get_metrics_by_vessel_class_id(
                vessel_class_id=vessel_class_id, year=year
            )
        )
        class_summary = _aggregate_class_metrics(class_metrics)

    return json.dumps(
        {
            "imo": imo,
            "vessel_name": vd.get("name") or vd.get("vessel_name"),
            "vessel_class_id": vessel_class_id,
            "vessel_class": vessel_class_name,
            "vessel_type": vd.get("vessel_type") or vd.get("vesselType"),
            "year": year,
            "vessel_metrics": _to_dict(vessel_metrics),
            "peer_class_summary": class_summary,
        },
        default=str,
    )


@mcp.tool()
async def get_market_rates_by_route_name(
    route_name: str,
    start_date: str,
    vessel_class_id: Optional[int] = None,
    end_date: Optional[str] = None,
    cargo_id: Optional[int] = None,
) -> str:
    """Get market rates by route name or route ID in one call.

    Combines get_market_rate_routes + get_market_rates. Searches routes
    for a case-insensitive partial match on route_name against both the
    route name (e.g. 'MR2 - Cont/USAC', 'VLCC - MEG/China') and the
    route ID (e.g. 'R27'). Industry codes like 'TC2' or 'TD3C' are NOT
    Signal Ocean route names — call get_market_rate_routes first to
    discover the exact name, then use it here.
    If no match is found, returns the full route list (id + name) so you
    can pick the correct term. start_date as YYYY-MM-DD (required).
    cargo_id: 0=Dirty, 1=Clean, 2=IMO.
    """
    from signal_ocean.market_rates.enums import CargoId

    routes = await anyio.to_thread.run_sync(
        lambda: _market_rate_routes_sync(vessel_class_id)
    )
    if not routes:
        return json.dumps({"error": "No routes found for the given vessel class"})

    # Route model serializes with PascalCase aliases: ID, Description
    name_lower = route_name.lower()
    matched_route = None
    for route in routes:
        rd = _to_dict(route)
        rdesc = str(rd.get("Description") or rd.get("description") or rd.get("name") or "").lower()
        rid = str(rd.get("ID") or rd.get("id") or rd.get("route_id") or "").lower()
        desc_match = rdesc and (name_lower in rdesc or rdesc in name_lower)
        id_match = rid and (name_lower in rid or rid in name_lower)
        if desc_match or id_match:
            matched_route = rd
            break

    if matched_route is None:
        available = [
            f"{_to_dict(r).get('ID') or _to_dict(r).get('id')} — {_to_dict(r).get('Description') or _to_dict(r).get('description')}"
            for r in routes
        ]
        return json.dumps(
            {"error": f"No route matching '{route_name}'", "available_routes": available}
        )

    route_id = str(
        matched_route.get("ID") or matched_route.get("id") or
        matched_route.get("route_id") or matched_route.get("Description") or
        matched_route.get("description")
    )
    sd = date.fromisoformat(start_date)
    ed = _parse_date(end_date)
    cid = CargoId(cargo_id) if cargo_id is not None else None

    rates = await anyio.to_thread.run_sync(
        lambda: _market_rates_api.get_market_rates(
            start_date=sd,
            route_id=route_id,
            vessel_class_id=vessel_class_id,
            end_date=ed,
            cargo_id=cid,
        )
    )
    result_rates = rates if isinstance(rates, (list, tuple)) else [rates]
    return json.dumps(
        {
            "matched_route": matched_route,
            "rates": [_to_dict(r) for r in result_rates],
        },
        default=str,
    )


def main() -> None:
    """Run the Signal Ocean MCP server."""
    mcp.run()
