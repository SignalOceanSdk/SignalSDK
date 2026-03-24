# v14.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Performance — Pydantic v2 Deserialisation

- Replaced the internal `parsing_helpers` deserialisation engine with [Pydantic v2](https://docs.pydantic.dev/latest/). All SDK models are now `pydantic.BaseModel` subclasses.
- Parsing time for large queries reduced by ~70% (from ~27% to ~14% of total wall time on a full `VoyageCondensed` fetch).
- Effective throughput improved from ~40 req/min to ~150 req/min on the condensed voyages endpoint.

## Performance — HTTP Connection Reuse

- `Connection` now uses a persistent `requests.Session` for all API calls, eliminating per-request TLS handshake overhead.
- Throughput on the first benchmark query improved from ~26 req/min to ~40 req/min; combined with the parsing improvements the sustained rate reaches ~155 req/min.
- `Connection` now supports `close()` and can be used as a context manager. Call `connection.close()` when you are done, or use `with Connection(...) as connection:` to ensure the underlying session is released.

```python
# Option A — explicit close
connection = Connection()
# ... use APIs ...
connection.close()

# Option B — context manager
with Connection() as connection:
    # ... use APIs ...
```

## Breaking Changes

- **Minimum Python version raised from 3.7 to 3.8.** Python 3.7 reached end-of-life in June 2023 and is no longer supported.
- **`pydantic>=2.0` is now a required dependency.** All SDK models are now Pydantic `BaseModel` subclasses. If your project pins `pydantic<2`, you will need to upgrade.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
