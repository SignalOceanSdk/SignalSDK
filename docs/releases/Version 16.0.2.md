# v16.0.2
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Bug Fixes

- Fixed PyPI upload failure caused by incorrect package name casing. The package name in `setup.py` has been normalized from `signal-ocean` to `signal_ocean` to match PyPI's required artifact filename format. Existing installs are unaffected — `pip install signal-ocean` continues to work as before.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
