The Signal Ocean SDK combines the power of Python and [Signal Ocean's APIs](https://apis.signalocean.com/) to give you access to a variety of shipping data available in [The Signal Ocean Platform](https://www.signalocean.com/platform).

# Installation

Install the SDK with pip:
```
pip install signal-ocean
```

The Signal Ocean SDK depends on the [pandas](https://pandas.pydata.org/) library for some of its data analysis features. Optional pandas dependencies are also optional in this SDK. If you plan to use data frame features like plotting or exporting to Excel, you need to install additional dependencies, for example:
```
pip install matplotlib openpyxl
```
For more information refer to [pandas documentation](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html#optional-dependencies).

# Getting Started

To use the SDK, you need to create an account in our [API Portal](https://apis.signalocean.com/) and subscribe to an API. Once you have a subscription key, put it inside an environment variable called `SIGNAL_OCEAN_API_KEY`.

Now you're ready to fetch some data:
```
from signal_ocean import PortAPI

port_api = PortAPI()
ports = port_api.get_ports()

print(ports)
```

If you don't want to use environment variables, want to use different keys for different APIs, or if you want to override the environment variables, you can configure your `Connection` when creating the API class:
```
from signal_ocean import VesselClassAPI, Connection

vessel_class_api = VesselClassAPI(Connection(api_key='YOUR KEY GOES HERE'))
vessel_classes = vessel_class_api.get_vessel_classes()

print(vessel_classes)
```

All API classes follow this pattern of configuration.

Check the docs for examples covering usage of our other APIs.
