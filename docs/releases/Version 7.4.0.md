# v7.4.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Scraped Cargoes API

- Upgraded endpoint to v5.0.
- Added `message_ids` and `external_message_ids` parameters in `get_cargoes` method.
- Added `external_message_id` and `subject` fields in `ScrapedCargo`.

## Scraped Fixtures API

- Upgraded endpoint to v5.0.
- Added `message_ids` and `external_message_ids` parameters in `get_fixtures` method.
- Added `external_message_id` and `subject` fields in `ScrapedFixture`.

## Scraped Lineups API

- Upgraded endpoint to v5.0.
- Added `message_ids` and `external_message_ids` parameters in `get_lineups` method.
- Added `external_message_id` field in `ScrapedLineup`.

## Scraped Positions API

- Upgraded endpoint to v5.0.
- Added `message_ids` and `external_message_ids` parameters in `get_positions` method.
- Added `external_message_id` and `subject` fields in `ScrapedPosition`.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
