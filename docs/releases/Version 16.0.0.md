# v16.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Pandas 3 Support

- The SDK is now compatible with pandas 3.x (requires Python 3.11+).
- `strictly-typed-pandas` has been removed as a dependency (it was not used by the SDK).

## Breaking Changes

- **Minimum pandas version remains `>=1.0.3`**, but pandas 3.x is now supported (upper bound raised from `<3` to `<4`).

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
