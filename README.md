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

To use the SDK, you need to create an account in our [API Portal](https://apis.signalocean.com/) and subscribe to an API.

Now you're ready to fetch some data. See our [examples](docs\examples) on how you can use our APIs.

# Building and contributing

Check [Contributing.md](Contributing.md) on how you can build and contribute this library. 
