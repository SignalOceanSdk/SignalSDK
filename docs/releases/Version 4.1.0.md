# v4.1.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Port Congestion API Integration

- Adds a Port Congestion API Wrapper (`PortCongestionAPI`)
- Refactors Waiting Time over Time to utilize the Port Congestion API wrapper instead of
  calculating it internally.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`