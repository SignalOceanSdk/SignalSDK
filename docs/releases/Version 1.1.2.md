# v1.1.2
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)


## Updated Scraped Fixtures API 
### Updated get_fixtures function
Change data type for field `received_date_from` from date to datetime.
Set field `received_date_from` Optional.
Set field `vessel_type` Optional.
Change data type for field `received_date_to` from date to datetime.
Change data type for field `updated_date_from` from date to datetime.
Change data type for field `updated_date_to` from date to datetime.

### Updated Scraped Fixtures model
Rename field `charterer_type` to `charter_type`

## Notebook examples update

### Update Scraped Fixtures API Example
Updated the example by using datetime instead of date for `received_date_to` field

### Add new example (Latest Received Scraped Fixtures)
This example uses the Scraped Fixture API in order to get the latest fixtures for tanker and dry.
The final results are exported to csv files.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`