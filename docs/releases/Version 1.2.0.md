# v1.2.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

# Added Scraped Cargoes API

## Scraped Cargoes API Methods
- `get_cargoes`: Retrieve cargoes within specific date range.
- `get_cargoes_by_cargo_ids`: Retrieve cargoes by `cargo_ids`.

# Added Scraped Positions API

## Scraped Positions API Methods
- `get_positions`: Retrieve positions for specific date range and/or specific IMOs.
- `get_positions_by_position_ids`: Retrieve positions by `position_ids`.

# Updated Scraped Fixtures API

## Updated Scraped Fixtures API models
- Added attribute `delivery_taxonomy` in `ScrapedFixture` class.
- Renamed attribute `scraped_year_build` to `scraped_year_built` in `ScrapedFixture` class.
- Renamed attribute `year_build` to `year_built` in `ScrapedFixture` class.
- Removed attribute `reported_fixture_date` from `ScrapedFixture` class.
- Added `ScrapedFixturesResponse` class.

## Updated Scraped Fixtures API Methods
- Added parameter in `get_fixtures` method `imos`.
- Renamed parameter `include_fixture_details` to `include_details`.
- Removed parameters `vessel_class_id`, `port_id`.
- Added method `get_fixtures_by_fixture_ids` to retrieve fixtures by `fixture_ids`.

## Updated Notebook Examples
- Removed LatestReceivedScrapedFixtures example.
- Updated Scraped Fixtures API Example to present the whole functionality.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`