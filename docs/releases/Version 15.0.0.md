# v15.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## MCP Server

Added an MCP (Model Context Protocol) server that exposes all Signal Ocean APIs as tools for AI assistants.

- Query vessel data, voyages, emissions, market rates, freight pricing, distances, port expenses, tonnage lists, and scraped market data using natural language from any MCP-compatible client (Claude, Cursor, Windsurf, Cline, and others).
- **69 tools** covering vessels, voyages, market rates, distances, port expenses, tonnage lists, emissions, valuations, freight pricing, scraped cargoes/fixtures/lineups/positions, geography, and companies.
- Install with `pip install signal-ocean[mcp]` and run with `python -m signal_ocean_mcp`.
- No AI vendor dependency required — only your existing Signal Ocean API key.
- See the [MCP Server documentation](../mcp-server.md) for configuration and usage examples.

### Composite tools

Higher-level tools that resolve names and combine multiple API calls into a single step:

- `get_market_rates_by_route_name` — look up rates by route name (e.g. "TD3C", "C5TC") without needing a route ID.
- `get_tonnage_list_and_market_rates` — fetch tonnage supply and the corresponding market rate in one call.
- `compare_port_expenses` — compare port costs across two or more ports by vessel class name, no IDs required.
- `get_vessels_by_operator` — list a fleet by company name, resolving the operator ID automatically.
- `get_vessel_supply` — ballasting/supply view combining historical tonnage list data.
- `get_vessel_emission_benchmark` — CII rating for a vessel compared to its peer class.
- `get_latest_voyage_emissions` — CO₂ and other emissions for a vessel's most recent completed voyage.

### Name resolution

All tools that previously required numeric IDs now also accept human-readable names:

- Vessel class name (e.g. `"Suezmax"`, `"VLCC"`) in place of `vessel_class_id` across tonnage, market rate, voyages, and valuation tools.
- Port name in place of `port_id` across distances, freight rates, freight pricing, port expenses, and tonnage tools.
- Charterer name in place of `charterer_id` in voyage search tools.
- Route name (e.g. `"MEG China"`, `"C5TC"`) in place of `route_id` in market rate tools.

### Performance

- All API instances are singletons sharing a single HTTP session for the server lifetime, eliminating per-request connection overhead.
- Static reference data (vessel classes, vessel types, market rate routes) is cached per process using `lru_cache`.
- All SDK calls are dispatched via `anyio.to_thread.run_sync` so the MCP event loop is never blocked.

### Reliability fixes

- Fixed serialisation for `HistoricalTonnageList` and market data date fields.
- Fixed Windows Claude Desktop compatibility: blank lines filtered from stdio transport.
- Fixed stdout pollution from SDK warnings that corrupted the MCP stdio transport.
- Fixed `compare_port_expenses` import and vessel-type resolution.
- Fixed `get_market_rates_by_route_name` PascalCase field mapping.
- Fixed route ID exact-match logic to prevent substring collisions.
- Fixed `get_vessel_supply` date range to avoid HTTP 400 on unpublished snapshots.
- Resolved ScrapedData API boolean query parameter encoding.

## Notes

- The `signal-ocean[mcp]` extra requires **Python 3.10 or later** (imposed by the `mcp` dependency). The core `signal-ocean` package continues to support Python 3.8+.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean[mcp] -U`

To upgrade without the MCP server: `pip install signal-ocean -U`
