# v1.0.4
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

- New api integration: Freight Rates API package

    - Added get_freight_pricing method:
    Exposed the corresponding endpoint of FreightRates API which provides freight rate given a load port, a discharge port and vessel class.

    - Added get_ports method:
    Exposed the corresponding endpoint of FreightRates API which fetches all available ports for which we can provide freight rates.

    - Added get_vessel_classes method:
    Added helper method that returns all available vessel classes for which we can provide freight rates.

- Live Tonnage list available under renamed Tonnage List API
    
    - Historical Tonnage List API is renamed to Tonnage List API. Old API libraries are deprecated and replacable 1-1 with the new api. Users can now recall data from Signal Ocean Tonnage List in a live format for any time of the day they want to.

- Deprecation of Historical Tonnage List API
    
    - Users should switch to the new Tonnage List API which replaces 100% the old Historical Tonnage List API.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`



