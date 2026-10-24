# v16.1.1
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Bug Fixes

Fixed `get_voyage_market_data` failing with a `ValidationError` when a matched
fixture contains a fractional quantity, for example `QuantityBuffer` equal to
`0.1` (a fraction of 1, meaning ±10%). The following `MatchedFixture` fields are
now `float` instead of `int`, in line with the API:
- `quantity`
- `quantity_buffer`
- `ballast_bonus_value`

Since version 14.0.0 a fractional value in these fields failed the whole call,
and before that it was silently truncated to `0`.

## Installation and Upgrade Notes

Update your package with: `pip install signal-ocean -U`
