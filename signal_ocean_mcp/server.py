"""Signal Ocean MCP Server.

Exposes Signal Ocean SDK APIs as MCP tools for use with
Claude and other MCP-compatible AI clients.
"""

import json
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
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


async def _resolve_vessel_class(vessel_class_id: Optional[int], vessel_class_name: Optional[str]):
    if vessel_class_id is not None:
        return vessel_class_id, None
    if not vessel_class_name:
        return None, "Provide vessel_class_id or vessel_class_name"
    classes = await anyio.to_thread.run_sync(_vessel_classes_sync)
    name_lower = vessel_class_name.lower()
    for vc in (classes or []):
        d = _to_dict(vc)
        cname = str(d.get("Name") or d.get("name") or "").lower()
        cid = d.get("ID") or d.get("id")
        if cname and (name_lower in cname or cname in name_lower):
            return cid, None
    return None, f"No vessel class found matching '{vessel_class_name}'"


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
async def get_vessels_by_vessel_class(
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    limit: int = 50,
) -> str:
    """Get vessels belonging to a specific vessel class.

    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'VLCC').

    WARNING: A major class (e.g. Suezmax, VLCC) contains hundreds of vessels and
    will return a very large response. Set limit to control the number returned
    (default 50). If you only need an IMO to pass to another tool, use
    search_vessel_imos instead — it returns just IMO numbers with much smaller payload.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
    vessels = await anyio.to_thread.run_sync(
        lambda: _vessels_api.get_vessels_by_vessel_class(vesselClass=vessel_class_id)
    )
    if vessels and limit:
        vessels = list(vessels)[:limit]
    return _serialize(vessels)


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
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    include_consumptions: bool = False,
    include_efficiency_metrics: bool = False,
    include_distances: bool = False,
    include_durations: bool = False,
    include_speed_statistics: bool = False,
    include_eu_emissions: bool = False,
) -> str:
    """Get emissions data for all vessels in a vessel class.

    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'VLCC').
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    year: Optional[int] = None,
) -> str:
    """Get emission metrics (CII, AER, EEOI) for all vessels in a class.

    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'VLCC').
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    vessel_class_name: Optional[str] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyage data for vessels.

    Filter by IMO, vessel class, vessel type ID, or start date (YYYY-MM-DD).
    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'Capesize').

    WARNING: Querying by vessel_class alone over a multi-week window returns
    thousands of voyages and will exceed the 1MB response cap. Always combine
    with a narrow date_from or filter by IMO. For class-level analysis, use
    get_voyages_advanced_search with additional port or date filters.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err and vessel_class_name:
        return json.dumps({"error": err})
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
    vessel_class_name: Optional[str] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get condensed voyage data (lighter payload than full voyages).

    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'Capesize').

    WARNING: Querying by vessel_class alone over a multi-week window returns
    thousands of records and will exceed the 1MB response cap. Always combine
    with a narrow date_from or filter by IMO.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err and vessel_class_name:
        return json.dumps({"error": err})
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
    vessel_class_name: Optional[str] = None,
    vessel_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
) -> str:
    """Get voyages in flat format (separate lists for voyages, events, details, geos).

    Useful for large datasets as it avoids deeply nested structures.
    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'Capesize').

    WARNING: Querying by vessel_class alone over a multi-week window returns
    thousands of records and will exceed the 1MB response cap. Always combine
    with a narrow date_from or filter by IMO.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err and vessel_class_name:
        return json.dumps({"error": err})
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
    vessel_class_name: Optional[str] = None,
    vessel_class_ids: Optional[list[int]] = None,
    vessel_type_id: Optional[int] = None,
    port_id: Optional[int] = None,
    port_ids: Optional[list[int]] = None,
    port_name: Optional[str] = None,
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
    Provide vessel_class_id or vessel_class_name (e.g. 'Suezmax', 'Capesize').
    Provide port_id or port_name (e.g. 'Ras Tanura', 'Rotterdam') — resolved automatically.
    Dates as YYYY-MM-DD.

    WARNING: Querying by vessel class alone over a wide date range returns
    thousands of voyages and will exceed the 1MB response cap. Always combine
    with port filters or narrow date ranges.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err and vessel_class_name:
        return json.dumps({"error": err})
    if port_name and port_id is None:
        port_id, err = await _resolve_tonnage_list_port(None, port_name)
        if err:
            return json.dumps({"error": err})
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
    vessel_class_name: Optional[str] = None,
) -> str:
    """Get available market rate routes, optionally filtered by vessel class.

    Route names follow Signal Ocean conventions (e.g. 'MR2 - Cont/USAC',
    'VLCC - MEG/China') rather than standard industry codes (TC2, TD3C).
    Provide vessel_class_id or vessel_class_name (e.g. 'MR2', 'VLCC') to filter.
    """
    if vessel_class_name and vessel_class_id is None:
        vessel_class_id, err = await _resolve_vessel_class(None, vessel_class_name)
        if err:
            return json.dumps({"error": err})
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
    loading_condition_id: int,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    port_from_id: Optional[int] = None,
    port_to_id: Optional[int] = None,
    port_from_name: Optional[str] = None,
    port_to_name: Optional[str] = None,
) -> str:
    """Get the sailing distance between two ports for a given vessel class.

    loading_condition_id: 1 = Laden, 2 = Ballast.
    Provide vessel class and ports by ID or name — all resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    loading_condition_id: int,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    port_from_id: Optional[int] = None,
    port_to_id: Optional[int] = None,
    port_from_name: Optional[str] = None,
    port_to_name: Optional[str] = None,
) -> str:
    """Get the sailing route between two ports for a given vessel class.

    Returns waypoints, distance, and route details.
    loading_condition_id: 1 = Laden, 2 = Ballast.
    Provide vessel class and ports by ID or name — all resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    loading_condition_id: int,
    start_lon: float,
    start_lat: float,
    end_lon: float,
    end_lat: float,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
) -> str:
    """Get the sailing distance between two coordinates.

    loading_condition_id: 1 = Laden, 2 = Ballast.
    Coordinates as decimal degrees (lon, lat).
    Provide vessel_class_id or vessel_class_name.
    """
    from signal_ocean.distances.vessel_class import VesselClass
    from signal_ocean.distances.models import Point

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    loading_condition_id: int,
    point_lon: float,
    point_lat: float,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    port_id: Optional[int] = None,
    port_name: Optional[str] = None,
) -> str:
    """Get the sailing distance from a coordinate to a port.

    loading_condition_id: 1 = Laden, 2 = Ballast.
    Provide vessel class and port by ID or name — all resolved automatically.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass
    from signal_ocean.distances.models import Point

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    """Search for shipping companies by name — operators, charterers, owners, managers.

    Use this to find a company ID before filtering voyages or vessels by operator.
    Returns company_id, name, and type. Partial name matching is supported.
    """
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

    NOTE: This endpoint returns 500 for some vessel_class_id / port combinations
    where model-vessel data is not available. If you get a 500, use get_port_expenses
    with a real vessel IMO from that class instead, or use the composite tool
    compare_port_expenses which handles this fallback automatically.
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
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    loading_port_id: Optional[int] = None,
    loading_port_name: Optional[str] = None,
    laycan_end_in_days: Optional[int] = None,
) -> str:
    """Get the current tonnage list for a loading port and vessel class.

    Shows available vessels near a port.
    Provide vessel class and port by ID or name — all resolved automatically.
    Example: vessel_class_name='Suezmax', loading_port_name='Ras Tanura'.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
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
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    loading_port_id: Optional[int] = None,
    loading_port_name: Optional[str] = None,
    laycan_end_in_days: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count_only: bool = False,
) -> str:
    """Get historical tonnage list for a port and vessel class over a date range.

    Dates as YYYY-MM-DD.
    Provide vessel class and port by ID or name — all resolved automatically.

    WARNING: Full vessel detail over multi-day windows can exceed the 1MB response
    cap even with a short laycan_end_in_days. Use count_only=True for supply-trend
    analysis — it returns {date: vessel_count} instead of full vessel records,
    cutting response size by 20-50x. For combined supply + market rate data,
    use get_tonnage_list_and_market_rates instead.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
    loading_port_id, err = await _resolve_tonnage_list_port(loading_port_id, loading_port_name)
    if err:
        return json.dumps({"error": err})

    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    htl = await anyio.to_thread.run_sync(
        lambda: _htl_api.get_historical_tonnage_list(
            loading_port=port,
            vessel_class=vc,
            laycan_end_in_days=laycan_end_in_days,
            start_date=sd,
            end_date=ed,
        )
    )
    if count_only:
        counts = {
            str(getattr(tl, "date", ""))[:10]: len(getattr(tl, "vessels", ()) or ())
            for tl in (htl or [])
            if str(getattr(tl, "date", ""))[:10]
        }
        return json.dumps({"count_by_date": counts})
    return _serialize(htl)


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
    """Get scraped cargo data from broker reports — cargo orders, cargo enquiries, requirements.

    Use this to answer: "what cargoes are being offered?", "what cargo orders were
    reported by brokers?", "what are the cargo requirements for tankers / dry bulk?"

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format (YYYY-MM-DDTHH:MM:SS).

    WARNING: Responses can be very large (hundreds of records, each with ~100 fields).
    Always use narrow date windows (1-6 hours max). Tanker data is especially dense.
    For large-volume or class-filtered cargo queries, prefer get_voyage_market_data_advanced
    with cargo_date_from/cargo_date_to parameters.
    """
    df = _parse_datetime(received_date_from)
    dt = _parse_datetime(received_date_to)
    return _serialize(
        await anyio.to_thread.run_sync(
            lambda: _scraped_cargoes_api.get_cargoes(
                vessel_type=vessel_type,
                received_date_from=df,
                received_date_to=dt,
                include_debug_info=False,
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
    """Get scraped fixture data from broker reports — charters fixed, vessel fixtures, chartering activity.

    Use this to answer: "what vessels were fixed recently?", "what charters were
    reported?", "what fixtures were done for tankers / dry bulk in the last few hours?"

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Dates as ISO format. Optionally filter by vessel IMO numbers.

    WARNING: Responses can be very large — tanker fixtures run 100-150 records/hour,
    each with ~100 fields. Always use narrow date windows (1-3 hours max) and filter
    by imos when possible. There is NO server-side vessel class filter on this endpoint.
    For class-filtered fixture queries, use get_voyage_market_data_advanced with
    vessel_class_ids and fixture_date_from/fixture_date_to parameters instead.
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
                include_debug_info=False,
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
    """Get scraped port lineup data — vessels at port, loading queue, port congestion reports.

    Use this to answer: "which vessels are in the lineup at [port]?", "what tankers
    are waiting to load at Ras Tanura / Basrah / Novorossiysk?", "how many vessels
    are in the loading queue at [terminal]?", "what is the port congestion at X?"

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Optionally filter by vessel IMO numbers.

    WARNING: Responses can be very large. Always use narrow date windows (1-6 hours max).
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
                include_debug_info=False,
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
    """Get scraped vessel position data — vessel locations, open positions, position lists.

    Use this to answer: "where is vessel X?", "what vessels are open in the
    North Sea?", "which tankers are reporting open positions near Singapore?",
    "what position list was reported for Aframax vessels?"

    vessel_type: 1=Tanker, 3=Dry, 6=LPG, 4=LNG, 5=Container.
    Optionally filter by vessel IMO numbers.

    WARNING: Responses can be very large. Always use narrow date windows (1-6 hours max).
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
                include_debug_info=False,
            )
        )
    )


# --- Composite Tools (collapse common multi-call patterns into single tool calls) ---


def _aggregate_class_metrics(metrics_result) -> dict:
    """Compute summary stats over per-vessel class emission metrics."""
    if metrics_result is None:
        return {}
    # VesselClassMetrics is a paginated wrapper with a .data List[VesselMetrics]
    if hasattr(metrics_result, "data"):
        items = list(metrics_result.data or [])
    else:
        items = list(metrics_result)
    if not items:
        return {"vessel_count": 0}

    cii_scores: list[float] = []
    rating_dist: dict[str, int] = {}
    for m in items:
        d = _to_dict(m)
        if not isinstance(d, dict):
            continue
        # Cii is a nested object; aliases are PascalCase (Value, Rating)
        cii = d.get("Cii") or d.get("cii") or {}
        if isinstance(cii, dict):
            score = cii.get("Value") or cii.get("value")
            if score is not None:
                try:
                    cii_scores.append(float(score))
                except (ValueError, TypeError):
                    pass
            rating = cii.get("Rating") or cii.get("rating")
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
    # VoyageCondensed uses 'horizon' (not 'voyage_horizon'); values: "Historic", "Historical"
    _hist = {"Historic", "Historical", "historic", "historical"}
    completed = [
        v for v in items
        if getattr(v, "end_date", None) is not None
        and getattr(v, "horizon", None) in _hist
    ]
    if not completed:
        completed = [v for v in items if getattr(v, "horizon", None) in _hist]
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
    # Vessel serializes with PascalCase aliases (VesselClassID, VesselClass, etc.)
    vessel_class_id = vd.get("VesselClassID") or vd.get("vessel_class_id")
    vessel_class_name = vd.get("VesselClass") or vd.get("vessel_class")

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
            "vessel_name": vd.get("VesselName") or vd.get("vessel_name"),
            "vessel_class_id": vessel_class_id,
            "vessel_class": vessel_class_name,
            "vessel_type": vd.get("VesselType") or vd.get("vessel_type"),
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
        id_match = rid and name_lower == rid  # exact match only — "r2" must not match "mr2"
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


@mcp.tool()
async def compare_port_expenses(
    port_names: list[str],
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    imo: Optional[int] = None,
    formula_calculation_date: Optional[str] = None,
) -> str:
    """Compare port expenses across multiple ports for a vessel class in one call.

    Eliminates the 5-7 call chain (port resolution → vessel lookup → per-port
    expenses) down to 1 data call per port.

    Provide 2+ port names (e.g. ["Rotterdam", "Fujairah"]) and one of:
    - vessel_class_name (e.g. "Suezmax", "VLCC", "Aframax") — resolves vessel_type_id
      from the class definition; no vessel fetch required
    - vessel_class_id — same resolution
    - imo — uses get_port_expenses with a real vessel (most specific, but requires a
      known IMO; do NOT call get_vessels_by_vessel_class to find one — it returns
      hundreds of records)

    formula_calculation_date: ISO datetime for expense calculation (default: now).

    Returns a ranked comparison of estimated port expenses across all requested ports.
    Use this instead of calling get_port_expenses_required_params + get_port_expenses_ports
    + get_port_model_vessel_expenses for each port.
    """
    calc_date = (
        datetime.fromisoformat(formula_calculation_date)
        if formula_calculation_date
        else datetime.utcnow()
    )

    vessel_type_id: Optional[int] = None
    resolved_class_name: Optional[str] = None

    if imo is not None:
        # Real-vessel path: use get_port_expenses per port
        results: list[dict] = []
        for port_name in port_names:
            port_id, err = await _resolve_port_expenses_port(None, port_name)
            if err:
                results.append({"port": port_name, "error": err})
                continue
            try:
                expenses = await anyio.to_thread.run_sync(
                    lambda pid=port_id: _port_expenses_api.get_port_expenses(imo=imo, port_id=pid)
                )
                ed = _to_dict(expenses)
                total = (ed.get("Total") or ed.get("total")) if isinstance(ed, dict) else None
                results.append({"port": port_name, "port_id": port_id, "total_usd": total, "details": ed})
            except Exception as exc:
                results.append({"port": port_name, "port_id": port_id, "error": str(exc)})
    else:
        # Model-vessel path: resolve vessel_type_id from the class definition
        vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
        if err:
            return json.dumps({"error": err})

        # Extract vessel_type_id from cached class list — no extra API call
        classes = await anyio.to_thread.run_sync(_vessel_classes_sync)
        vessel_type_id: Optional[int] = None
        resolved_class_name: Optional[str] = None
        for vc in (classes or []):
            d = _to_dict(vc)
            cid = d.get("ID") or d.get("id")
            if cid == vessel_class_id:
                vessel_type_id = d.get("VesselTypeID") or d.get("vessel_type_id")
                resolved_class_name = d.get("Name") or d.get("name")
                break

        if vessel_type_id is None:
            return json.dumps({"error": f"Could not determine vessel_type_id for class {vessel_class_id}"})

        results = []
        for port_name in port_names:
            port_id, err = await _resolve_port_expenses_port(None, port_name)
            if err:
                results.append({"port": port_name, "error": err})
                continue
            try:
                # vessel_class_id intentionally omitted (0 default) — non-zero values
                # return 500 from the upstream API for most class/port combinations
                expenses = await anyio.to_thread.run_sync(
                    lambda pid=port_id: _port_expenses_api.get_port_model_vessel_expenses(
                        port_id=pid,
                        vessel_type_id=vessel_type_id,
                        formula_calculation_date=calc_date,
                    )
                )
                ed = _to_dict(expenses)
                total = (ed.get("Total") or ed.get("total")) if isinstance(ed, dict) else None
                results.append({"port": port_name, "port_id": port_id, "total_usd": total, "details": ed})
            except Exception as exc:
                results.append({"port": port_name, "port_id": port_id, "error": str(exc)})

    def _sort_key(r: dict):
        t = r.get("total_usd")
        return (0, float(t)) if t is not None else (1, 0)

    results.sort(key=_sort_key)
    return json.dumps(
        {
            "vessel_class": resolved_class_name if imo is None else None,
            "vessel_type_id": vessel_type_id if imo is None else None,
            "imo_used": imo,
            "comparison": results,
        },
        default=str,
    )


@mcp.tool()
async def get_vessel_valuations_for_class(
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    max_vessels: int = 200,
    max_staleness_days: Optional[int] = 30,
) -> str:
    """Get latest valuations for all vessels in a vessel class in one call.

    Combines get_vessels_by_vessel_class + get_vessel_valuations_for_list.
    Avoids the oversized-response problem: fetches vessels internally, extracts
    only IMOs, then returns the (much smaller) valuation objects.

    vessel_class_name: e.g. 'Suezmax', 'VLCC', 'Capesize'.
    max_vessels: cap on how many vessels to include (default 200). Set lower
    for faster responses; the first N vessels in the class are used.
    max_staleness_days: drop valuations whose updated_date is older than this
        many days (default 30). Pass None to return all valuations regardless
        of age. Stale entries (e.g. valuations last updated years ago) are
        excluded from the response but counted in stale_count for transparency.

    Returns current valuations plus stale_count for excluded entries.
    Use this instead of calling get_vessel_classes + get_vessels_by_vessel_class
    + get_vessel_valuations_for_list separately.
    """
    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})

    vessels = await anyio.to_thread.run_sync(
        lambda: _vessels_api.get_vessels_by_vessel_class(vesselClass=vessel_class_id)
    )
    if not vessels:
        return json.dumps({"error": f"No vessels found for vessel class {vessel_class_id}"})

    imo_list = [v.imo for v in list(vessels)[:max_vessels] if v.imo]
    if not imo_list:
        return json.dumps({"error": "No IMOs found for vessels in this class"})

    valuations = await anyio.to_thread.run_sync(
        lambda: _vessel_valuations_api.get_latest_valuations_for_list_of_vessels(imo_list)
    )

    all_vals = list(valuations) if valuations else []
    if max_staleness_days is not None:
        cutoff = datetime.utcnow() - timedelta(days=max_staleness_days)
        current, stale = [], []
        for v in all_vals:
            ud = getattr(v, "updated_date", None)
            try:
                updated = datetime.fromisoformat(str(ud).replace("Z", "+00:00").replace("+00:00", ""))
                (current if updated >= cutoff else stale).append(v)
            except (ValueError, TypeError):
                current.append(v)
    else:
        current, stale = all_vals, []

    return json.dumps(
        {
            "vessel_class_id": vessel_class_id,
            "vessel_count": len(imo_list),
            "current_count": len(current),
            "stale_count": len(stale),
            "max_staleness_days": max_staleness_days,
            "valuations": [_to_dict(v) for v in current],
        },
        default=str,
    )


@mcp.tool()
async def get_distance_matrix_from_port(
    origin_port_name: str,
    destination_port_names: list[str],
    loading_condition_id: int,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
) -> str:
    """Get sailing distances from one origin port to multiple destination ports in one call.

    Collapses the per-port loop (N × get_port_to_port_distance) into a single tool call.
    loading_condition_id: 1 = Laden, 2 = Ballast.
    Provide vessel class by name (e.g. 'Suezmax', 'VLCC') or ID.

    Returns a table of distances sorted by nautical miles, useful for comparing
    route options or building distance matrices for freight analysis.
    """
    from signal_ocean.distances.port import Port
    from signal_ocean.distances.vessel_class import VesselClass

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
    origin_port_id, err = await _resolve_distances_port(None, origin_port_name)
    if err:
        return json.dumps({"error": err})

    vc = VesselClass(id=vessel_class_id, name="")
    pf = Port(id=origin_port_id, name="")

    rows: list[dict] = []
    for dest_name in destination_port_names:
        dest_port_id, err = await _resolve_distances_port(None, dest_name)
        if err:
            rows.append({"destination": dest_name, "error": err})
            continue
        pt = Port(id=dest_port_id, name="")
        try:
            dist = await anyio.to_thread.run_sync(
                lambda pt=pt: _distances_api.get_port_to_port_distance(
                    vessel_class=vc,
                    loading_condition_id=loading_condition_id,
                    port_from=pf,
                    port_to=pt,
                )
            )
            rows.append({"destination": dest_name, "port_id": dest_port_id, "distance_nm": float(dist) if dist else None})
        except Exception as exc:
            rows.append({"destination": dest_name, "port_id": dest_port_id, "error": str(exc)})

    rows.sort(key=lambda r: (r.get("distance_nm") is None, r.get("distance_nm") or 0))
    return json.dumps(
        {
            "origin": origin_port_name,
            "origin_port_id": origin_port_id,
            "vessel_class_id": vessel_class_id,
            "loading_condition": "Laden" if loading_condition_id == 1 else "Ballast",
            "distances": rows,
        },
        default=str,
    )


@mcp.tool()
async def get_tonnage_list_and_market_rates(
    start_date: str,
    end_date: str,
    vessel_class_id: Optional[int] = None,
    vessel_class_name: Optional[str] = None,
    loading_port_id: Optional[int] = None,
    loading_port_name: Optional[str] = None,
    laycan_end_in_days: int = 30,
    route_name: Optional[str] = None,
    cargo_id: Optional[int] = None,
) -> str:
    """Get historical supply trend and market rates together in one call.

    Replicates the "Combined Examples" notebook pattern: vessel count per day
    (supply) alongside market rates for the same period, ready for correlation
    analysis without any post-processing.

    vessel_class_name: e.g. 'MR2', 'VLCC', 'Suezmax' — resolves automatically.
    loading_port_name: e.g. 'ARA', 'Ras Tanura' — resolves automatically.
    laycan_end_in_days: how far ahead to count open vessels (default 30).
    route_name: partial match against route description or exact route ID
      (e.g. 'MR2 - Cont/USAC', 'R27'). If omitted, returns supply trend only.
    cargo_id: 0=Dirty, 1=Clean, 2=IMO (used for market rates only).
    Dates as YYYY-MM-DD.

    Returns:
      supply_by_date: {date: vessel_count} aggregated from historical tonnage list.
      market_rates: list of rate records for the matched route (empty if no route_name).
      matched_route: the route record used for market rates.
    """
    from signal_ocean.tonnage_list.models import Port, VesselClass
    from signal_ocean.market_rates.enums import CargoId

    vessel_class_id, err = await _resolve_vessel_class(vessel_class_id, vessel_class_name)
    if err:
        return json.dumps({"error": err})
    loading_port_id, err = await _resolve_tonnage_list_port(loading_port_id, loading_port_name)
    if err:
        return json.dumps({"error": err})

    port = Port(id=loading_port_id, name="")
    vc = VesselClass(id=vessel_class_id, name="")
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    # Fetch historical tonnage list and aggregate vessel counts by date
    htl = await anyio.to_thread.run_sync(
        lambda: _htl_api.get_historical_tonnage_list(
            loading_port=port,
            vessel_class=vc,
            laycan_end_in_days=laycan_end_in_days,
            start_date=sd,
            end_date=ed,
        )
    )
    supply_by_date: dict[str, int] = {}
    if htl:
        for tl in htl:
            date_str = str(getattr(tl, "date", ""))[:10]
            if date_str:
                # TonnageList.vessels is a Tuple[Vessel, ...], not the iterable itself
                supply_by_date[date_str] = len(getattr(tl, "vessels", ()) or ())

    # Fetch market rates if a route name was provided
    matched_route: Optional[dict] = None
    rate_records: list = []
    if route_name:
        routes = await anyio.to_thread.run_sync(
            lambda: _market_rate_routes_sync(vessel_class_id)
        )
        name_lower = route_name.lower()
        for route in (routes or []):
            rd = _to_dict(route)
            rdesc = str(rd.get("Description") or rd.get("description") or "").lower()
            rid = str(rd.get("ID") or rd.get("id") or "").lower()
            if (rdesc and (name_lower in rdesc or rdesc in name_lower)) or (rid and name_lower == rid):
                matched_route = rd
                break

        if matched_route:
            route_id = str(matched_route.get("ID") or matched_route.get("id") or matched_route.get("Description"))
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
            rate_records = rates if isinstance(rates, (list, tuple)) else ([rates] if rates else [])

    return json.dumps(
        {
            "vessel_class_id": vessel_class_id,
            "loading_port_id": loading_port_id,
            "date_range": {"start": start_date, "end": end_date},
            "supply_by_date": supply_by_date,
            "matched_route": matched_route,
            "market_rates": [_to_dict(r) for r in rate_records],
        },
        default=str,
    )


@mcp.tool()
async def get_vessels_by_operator(
    company_name: Optional[str] = None,
    company_id: Optional[int] = None,
    lookback_days: int = 30,
) -> str:
    """Get all vessels currently operated by a shipping company in one call.

    Use this to answer: "what vessels does [company] operate?", "show me the
    fleet of [operator]", "which ships are managed by [company]?",
    "list all EPS / Thenamaris / Tsakos vessels."

    The VesselsAPI has no operator filter, so this works by querying recent
    voyages (last lookback_days days) for the operator and extracting unique
    vessels. Resolves company name automatically via search_companies.

    company_name: partial name match (e.g. 'EPS', 'Thenamaris', 'Tsakos').
    company_id: use directly if already known.
    lookback_days: how far back to look for voyages (default 30). Increase
        if the fleet appears incomplete for less active operators.

    Returns unique vessels (imo, name, class, type, dwt) seen under that
    operator in the lookback window.
    """
    # Resolve company name → ID
    if company_id is None:
        if not company_name:
            return json.dumps({"error": "Provide company_name or company_id"})
        companies = await anyio.to_thread.run_sync(
            lambda: _companies_api.get_companies(name=company_name)
        )
        companies = list(companies or [])
        if not companies:
            return json.dumps({"error": f"No company found matching '{company_name}'"})
        first = companies[0]
        cd = _to_dict(first)
        company_id = cd.get("ID") or cd.get("Id") or cd.get("id") or cd.get("CompanyId") or cd.get("company_id")
        resolved_name = cd.get("Name") or cd.get("name") or company_name
        if company_id is None:
            return json.dumps({"error": f"Could not extract company ID for '{company_name}'"})
    else:
        resolved_name = company_name or str(company_id)

    # Get recent voyages for this operator to extract unique vessels
    from_date = (datetime.utcnow() - timedelta(days=lookback_days)).date()
    voyages = await anyio.to_thread.run_sync(
        lambda: _voyages_api.get_voyages_by_advanced_search(
            commercial_operator_id=company_id,
            start_date_from=from_date,
            hide_events=True,
            hide_event_details=True,
            hide_market_info=True,
        )
    )

    # Extract unique vessels directly from voyage records — no per-vessel API calls needed
    seen: dict[int, dict] = {}
    for v in (voyages or []):
        vd = _to_dict(v)
        imo = vd.get("IMO") or vd.get("Imo") or vd.get("imo")
        if not imo or imo in seen:
            continue
        seen[imo] = {
            "imo": imo,
            "name": vd.get("VesselName") or vd.get("vessel_name"),
            "vessel_class_id": vd.get("VesselClassID") or vd.get("vessel_class_id"),
            "vessel_type_id": vd.get("VesselTypeID") or vd.get("vessel_type_id"),
            "vessel_type": vd.get("VesselType") or vd.get("vessel_type"),
            "dwt": vd.get("Deadweight") or vd.get("deadweight"),
        }

    vessels = sorted(seen.values(), key=lambda x: x.get("name") or "")

    return json.dumps({
        "company_id": company_id,
        "company_name": resolved_name,
        "lookback_days": lookback_days,
        "vessel_count": len(vessels),
        "vessels": vessels,
        **({"note": f"No voyages found for this operator in the last {lookback_days} days"} if not vessels else {}),
    }, default=str)


def main() -> None:
    """Run the Signal Ocean MCP server."""
    mcp.run()
