# Welcome to the Signal SDK

The Signal Ocean SDK combines the power of Python and [Signal Ocean's APIs](https://signalprodapims.developer.azure-api.net/) to give you access to a variety of shipping data available in [The Signal Ocean Platform](https://www.signalocean.com/platform).


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  

[The Signal Ocean SDK GitHub repository](https://github.com/SignalOceanSdk/SignalSDK/):  
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/SignalOceanSdk/SignalSDK/graphs/commit-activity)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/SignalOceanSdk/SignalSDK/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/signaloceansdk/signalsdk.svg)](https://GitHub.com/SignalOceanSDk/SignalSDK/contributors/)

[The Signal Ocean PyPi](https://pypi.org/project/signal-ocean/):  
[![PyPI status](https://img.shields.io/pypi/status/signal-ocean.svg)](https://pypi.org/project/signal-ocean/)
[![PyPI license](https://img.shields.io/pypi/l/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)
[![PyPI download total](https://img.shields.io/pypi/dm/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Installation

Install the SDK with pip:
```py
pip install signal-ocean
```

The Signal Ocean SDK depends on the [pandas](https://pandas.pydata.org/) library for some of its data analysis features. Optional pandas dependencies are also optional in this SDK. If you plan to use data frame features like plotting or exporting to Excel, you need to install additional dependencies, for example:
```
pip install matplotlib openpyxl
```
For more information refer to [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#optional-dependencies).

## Getting Started

To use the SDK, you need to create an account in our [API Portal](https://signalprodapims.developer.azure-api.net/) and subscribe to an API. Once you have a subscription key, put it inside an environment variable called `SIGNAL_OCEAN_API_KEY`.

Now you're ready to fetch some data:
```py
from signal_ocean import PortAPI

port_api = PortAPI()
ports = port_api.get_ports()

print(ports)
```

If you don't want to use environment variables, want to use different keys for different APIs, or if you want to override the environment variables, you can configure your `Connection` when creating the API class:
```py
from signal_ocean import VesselClassAPI, Connection

vessel_class_api = VesselClassAPI(Connection(api_key='YOUR KEY GOES HERE'))
vessel_classes = vessel_class_api.get_vessel_classes()

print(vessel_classes)
```

All API classes follow this pattern of configuration.

Check the docs for examples covering usage of our other APIs.
