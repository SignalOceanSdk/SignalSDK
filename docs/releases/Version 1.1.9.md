# v1.1.9
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## New api integration: Voyage Market Data API package
Created the SDK for Voyage Market Data API

### Added get_voyage_market_data method.
Exposed the corresponding endpoint of Voyage Market Data API.

### Two examples added.
VLCC Market rate calculation between A.Gulf and China
Number of fixtures per month, grouped by status for VLCCs

### Updated helper function request_helpers.py
Added Optional argument for nested data info on response

## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`