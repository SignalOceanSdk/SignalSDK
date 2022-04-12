# v1.1.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)


## Removed OilX Cargo Tracking API Package
## Added Scraped Fixtures API

The goal of Scraped Data APIs is to collect and return the fixtures by the given filters.  

## Added get_fixtures
Method to retrieve the fixtures data. 
The required parameters of this function are:
 
`received_date_from`: The received fixtures should have received date greater than this date 

`vessel_type`: The vessel type of the vessels

Also, the user can request fixtures for a specific vessel class or/and using a port id 

The funtion returns a list of Scraped Fixtures. The fields of Scraped fixtures 
are defined in models file 

## Notebook examples update

### ScrapedFixturesAPI
Example which describes how the user can extract the fixtures for VLCC/Aframax in the last 7 days.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`