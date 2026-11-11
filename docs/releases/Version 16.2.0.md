# v16.2.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## New Features

Added the Supply API module, `signal_ocean.supply`. It gives vessel supply
with more than 150 filters, daily history since 2014 and a live view.
- `SupplyAPI.get_supply_trend`: vessel counts per day for a date range.
- `SupplyAPI.get_historical_supply`: the vessels of one past day.
- `SupplyAPI.get_live_supply`: the vessels now.
- `SupplyAPI.get_supply_templates`: 28 Baltic route templates (for example
  `TD3C`, `C5`, `P6`). Pass a route code as `template` to any method, and add
  filters to change single template values.
- `to_data_frame()` on the trend and vessel results.

Added the MCP tools `get_supply_trend`, `get_historical_supply`,
`get_live_supply` and `get_supply_templates`.

## Documentation

Added a Supply page with six example notebooks. The three Combined Examples
now use the Supply API instead of the Historical Tonnage List.

## Installation and Upgrade Notes

Update your package with: `pip install signal-ocean -U`
