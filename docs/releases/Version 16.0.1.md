# v16.0.1
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Bug Fixes

Fixed incorrect field name casing during deserialization. Affected modules and fields are:
- Scraped Fixtures API
   - BrokerId
- Scraped Lineups API
  - ScrapedETA
  - ETA
  - ScrapedETB
  - ETB
  - ScrapedETD
  - ETD
- Scraped Tonnages API
  - LastCargoTypesIDs

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
