# v1.1.7
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Updated Voyages API models.
Added new attributes in Voyage class: `horizon_id, pit_vessel_name, year_built, suez_crossing, panama_crossing, canakkale_crossing, bosporus_crossing`.
Also added new attribute in VoyageEventDetail class: `sts_id`.

### Added new VoyageCondensed model.
Contains information about a single voyage of a vessel and details the events that took place during the voyage.

### Added new Voyages API methods.
New methods: `get_voyages_condensed, get_incremental_voyages_condensed, get_voyages_flat_by_advanced_search, get_voyages_condensed_by_advanced_search`.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`