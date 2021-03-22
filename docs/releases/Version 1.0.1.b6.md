# v1.0.1b6
Download here:

[![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Voyages API package
### Added first_load_arrival_date / event_date fields
Two new fields exposed through the VoyageData API:

`first_load_arrival_date`: The arrival date of the first load has been added to the root level to easily calculate ballast leg of the voyage.
`event_date`: The timestamp of the specific event, for instantaneous events e.g. VoyageStart

### Adding extra information about voyage on the response
`HasManualEntries`: Boolean. True if the fused matched fixture on a voyage contains at least one (partial or full) fixture input by a user. It indicates that there is additional information input by a user in addition to what received through market reports only

`BallastDistance`: Travelled distance in nautical miles between the last discharge port of the previous voyage and the first load port of the current voyage. It is computed based on AIS data. It includes the whole period between the two port calls and non operational stops as well. Accuracy depends on AIS coverage.

`LadenDistance`: Travelled distance in nautical miles between the first load port and the last discharge port of the same voyage. It is computed based on AIS data. Accuracy depends on AIS coverage.

## Distances API package
### Add minimize_seca restriction
`minimize_seca`: Determines whether or not to minimize distance travelled through SECA areas.


## Historical API package
### Split large HTL date ranges into multiple calls
Split calls that fetch data from more than a year to smaller chunks to avoid network timeouts.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`



