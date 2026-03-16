# v14.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Performance — Pydantic v2 Deserialisation

- Replaced the internal `parsing_helpers` deserialisation engine with [Pydantic v2](https://docs.pydantic.dev/latest/). All SDK models are now `pydantic.BaseModel` subclasses.
- Parsing time for large queries reduced by ~70% (from ~27% to ~14% of total wall time on a full `VoyageCondensed` fetch).
- Effective throughput improved from ~120 req/min to ~155 req/min on the condensed voyages endpoint.
- `pydantic>=2.0` is now a required dependency.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
