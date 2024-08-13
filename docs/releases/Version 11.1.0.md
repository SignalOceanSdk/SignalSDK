# v11.1.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Voyages Data API

- Added missing fields and updated descriptions
    - Voyage: `cargo_group_source_id, cargo_group_source, torres_strait_crossing, magellan_strait_crossing, great_belt_crossing`
    - VoyageEvent: `event_type_id, event_horizon_id, port_unlocode`
    - VoyageCondenced: `starting_port_unlocode, first_load_port_unlocode, last_discharge_port_unlocode`

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
