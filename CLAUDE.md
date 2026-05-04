# Claude Code Guidelines for SignalSDK

## MCP Server Sync Rule

`signal_ocean_mcp/server.py` wraps every public Signal Ocean SDK API as an MCP tool.
**Keep it in sync whenever the SDK changes.**

### When a Signal Ocean API module is modified

- **New public method added** → add a corresponding `@mcp.tool()` async function in `server.py`.
- **Method signature changed** (renamed param, new optional param, return type change) → update the matching tool function and its docstring.
- **Method removed or renamed** → remove or rename the corresponding tool in `server.py`.

### When a new Signal Ocean API module is integrated

1. Import the new `*API` class at the top of `server.py`.
2. Declare a module-level `_<name>_api: <Name>API` singleton variable.
3. Instantiate it inside `_lifespan` using the shared `_conn`.
4. Expose each public method as an `@mcp.tool()` async function using `anyio.to_thread.run_sync`.
5. If the API returns static/reference data (e.g. enumeration lists), add an `@lru_cache(maxsize=None)` helper like the existing `_vessel_classes_sync` pattern.

### Covered APIs (as of initial implementation)

| SDK module | API class | MCP tools prefix |
|---|---|---|
| `companies` | `CompaniesAPI` | `search_companies`, `get_company` |
| `distances` | `DistancesAPI` | `get_*_distance`, `get_*_route` |
| `freight_pricing` | `FreightPricingAPI` | `get_freight_pricing*` |
| `freight_rates` | `FreightRatesAPI` | `get_freight_rate*` |
| `geos` | `GeosAPI` | `get_areas`, `get_countries`, `get_ports_geo`, `get_geo_assets` |
| `historical_tonnage_list` | `HistoricalTonnageListAPI` | `get_historical_tonnage_list` |
| `market_rates` | `MarketRatesAPI` | `get_market_rate*` |
| `port_expenses` | `PortExpensesAPI` | `get_port_expenses*` |
| `tonnage_list` | `TonnageListAPI` | `get_tonnage_list*` |
| `vessel_consumptions` | `VesselConsumptionsAPI` | `get_vessel_*_consumptions` |
| `vessel_emissions` | `VesselEmissionsAPI` | `get_vessel_emissions*`, `get_voyage_emissions` |
| `vessel_valuations` | `VesselValuationsAPI` | `get_vessel_valuation*` |
| `vessels` | `VesselsAPI` | `get_vessel*`, `search_vessel*`, `get_vessel_classes`, `get_vessel_types` |
| `voyages` | `VoyagesAPI` | `get_voyages*` |
| `voyages_market_data` | `VoyagesMarketDataAPI` | `get_voyage_market_data*` |
| `scraped_cargoes` | `ScrapedCargoesAPI` | `get_scraped_cargoes` |
| `scraped_fixtures` | `ScrapedFixturesAPI` | `get_scraped_fixtures` |
| `scraped_lineups` | `ScrapedLineupsAPI` | `get_scraped_lineups` |
| `scraped_positions` | `ScrapedPositionsAPI` | `get_scraped_positions` |

**Not yet covered** (exist in `signal_ocean/` but have no MCP tools):
- `port_api.py` / `vessel_class_api.py` — older top-level APIs; evaluate whether they overlap with newer modules before adding.
