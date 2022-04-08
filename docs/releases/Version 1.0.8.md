# v1.0.8
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Voyages API package

### Added get_vessel_classes / get_vessel_types / get_imos methods

Three new methods exposed through the VoyageData API:

`get_vessel_classes`: The purpose of this method is to retrieve all available vessel classes. It can be called also using the newly added VesselClassFilter, which allows
filtering the response based on a string.

`get_vessel_types `: The purpose of this method is to retrieve all available vessel types. It can be called also using the newly added VesselTypeFilter, which allows
filtering the response based on a string.

`get_imos`: The purpose of this method is to retrieve all available vessels. It can be called also using the newly added VesselFilter, which allows
filtering vessel names based on a string.

## Notebook examples additions

### Get available vessel types, vessel classes, vessels
Added a simple notebook example how to use the aforementioned methods.

## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`