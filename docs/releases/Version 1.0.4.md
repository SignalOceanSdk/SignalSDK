# v1.0.4
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

- New api integration: Freight Rates API package

    - Added get_freight_pricing method:
    Exposed the corresponding endpoint of FreightRates API which provides freight rate given a load port, a discharge port and vessel class.

    - Added get_ports method:
    Exposed the corresponding endpoint of FreightRates API which fetches all available ports for which we can provide freight rates.

    - Added get_vessel_classes method:
    Added helper method that returns all available vessel classes for which we can provide freight rates.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`



