# v15.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## MCP Server

- Added an MCP (Model Context Protocol) server that exposes all Signal Ocean APIs as tools for AI assistants.
- Query vessel data, voyages, emissions, market rates, freight pricing, distances, port expenses, tonnage lists, and scraped market data using natural language from any MCP-compatible client (Claude, Cursor, Windsurf, Cline, and others).
- Install with `pip install signal-ocean[mcp]` and run with `python -m signal_ocean_mcp`.
- No AI vendor dependency required — only your existing Signal Ocean API key.
- See the [MCP Server documentation](../mcp-server.md) for configuration and usage examples.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean[mcp] -U`

To upgrade without the MCP server: `pip install signal-ocean -U`
