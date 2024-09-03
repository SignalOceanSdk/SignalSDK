# v12.0.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Vessels API

- Added missing fields `BowChainStopperDetailsAsStr, BowChainStoppersFitted,NumberOfBowChainStoppers, NumberOfCranes, NumberOfGrabs, NumberOfHatches`
- Fix mapping of fields `IMOType1, IMOType2, IMOType3` so they can load data
- Rename `te_u14` to `teu14` (Breaking Change)

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`
