# Supply

The Supply API tells you which vessels are available for a market segment,
and how many. It has daily history since 2014 and a live view of today. You
can filter on more than 150 fields: vessel class or size, open location and
date, commercial status, voyage state, AIS position, custom ETAs to a port,
and vessel particulars.

You need your own API key with access to the Supply API. Your subscription
also sets the vessel classes that you can query. A request for a vessel class
that your key cannot access fails with an error (HTTP 403).

## Methods

| Method | Use it for | Dates |
|---|---|---|
| `get_supply_trend` | Vessel counts per day, for trends and charts | A start date and an end date |
| `get_historical_supply` | The list of vessels on one past day | One day |
| `get_live_supply` | The list of vessels now | Always now |

All three methods take the same filters (`SupplyFilter`), a Baltic route
`template`, or both. Each filter needs a vessel class (`vessel_class`), or a
size band (`vessel_type`, `defining_size` and `size` together).

## Examples

### Supply trend with filters

```python
from datetime import date

from signal_ocean import Connection
from signal_ocean.supply import (
    CommercialAvailabilityFilter,
    FromToRange,
    GeoLocation,
    IncludeExcludeFilter,
    LocationTaxonomy,
    SupplyAPI,
    SupplyFilter,
    VesselClass,
)

api = SupplyAPI(Connection("YOUR_API_KEY"))

# Aframax tankers that open in Houston (port 3853) within 20 days,
# with commercial data updated in the last 5 days.
filters = SupplyFilter(
    vessel_class=VesselClass.AFRAMAX,
    commercial_availability=CommercialAvailabilityFilter(
        open_location=IncludeExcludeFilter(
            values=[GeoLocation(geo_id=3853, location_taxonomy=LocationTaxonomy.PORT)]
        ),
        open_date_relative_offset=FromToRange(from_=-5, to=20),
        latest_updated_date_relative_offset=FromToRange(from_=-5, to=0),
    ),
)

trend = api.get_supply_trend(date(2026, 10, 1), date(2026, 10, 31), filters=filters)
trend.to_data_frame()  # index: date, column: supply
```

### A Baltic route template with one change

```python
from signal_ocean.supply import MinMaxRange, VesselParticularsFilter

# TD3C, but with vessels up to 20 years old instead of 15.
# All other TD3C filters stay as they are.
trend = api.get_supply_trend(
    date(2026, 10, 1),
    date(2026, 10, 31),
    template="TD3C",
    filters=SupplyFilter(
        vessel_particulars=VesselParticularsFilter(vessel_age=MinMaxRange(max=20))
    ),
)
```

### Live supply as a data frame

```python
live = api.get_live_supply(template="TD25")
frame = live.to_data_frame()  # one row per vessel
frame[["imo", "open_location", "open_date_to", "eta_TD25"]]
```

The `Column` class lists the column names. Each ETA configuration adds
columns named after its `id`, for example `eta_TD25` and
`eta_distance_TD25`.

## How filters and templates combine

- A filter field that you set replaces the template's value for that field
  only. All other template filters stay.
- A list that you set replaces the template's list. It is not added to it.
- Set a field to `None` to remove that template filter.
- `vessel_class` replaces the template's size band (`vessel_type`,
  `defining_size` and `size`), and a size band replaces the template's
  `vessel_class`.
- An absolute date range, for example `open_date`, replaces the template's
  relative window for the same field.

## Baltic route templates

Pass a route code as `template`. Codes are not case sensitive. Call
`api.get_supply_templates()` to get the full definition of each template.

| Code | Template |
|---|---|
| TD1 | VLCC US Gulf Supply 30 Days (TD1) |
| TD3C | VLCC Arabian Gulf Supply 18 Days (TD3C) |
| TD15 | VLCC West Africa Supply 20 Days (TD15) |
| TD23 | Suezmax US Gulf Supply 20 Days (TD23) |
| TD20 | Suezmax West Africa Supply 20 Days (TD20) |
| TD6 | Suezmax Black Sea Supply 20 Days (TD6) |
| TD25 | Aframax US Gulf Supply 10 Days (TD25) |
| TD19 | Aframax Mediterranean Supply 10 Days (TD19) |
| TD7 | Aframax Continent Supply 10 Days (TD7) |
| TD8 | Aframax Arabian Gulf Supply 15 Days (TD8) |
| TC14 | MR2 US Gulf Supply 7 Days (TC14) |
| TC2 | MR2 Continent Supply 10 Days (TC2) |
| TC12 | MR2 Far East Supply 10 Days (TC12) |
| TC6 | MR1 Mediterranean Supply 10 Days (TC6) |
| TC1 | LR2 Arabian Gulf Supply Next 30 Days |
| TC5 | LR1 Arabian Gulf Supply Next 30 Days |
| C3 | Capesize Brazil 40 days ballasters (C3) |
| C5 | Capesize W Australia 15 days ballasters (C5) |
| C7 | Capesize Atlantic ballasters (C7) |
| P6 | Panamax ECSA 40 days ballasters (P6) |
| P1 | Panamax Atlantic ballasters (P1) |
| P3 | Panamax WCNA 20 days ballasters (P3) |
| P5 | Panamax Marketed SE Asia open 7 days (P5) |
| S5 | Supramax Marketed ECSA ETA 20days (S5) |
| S2 | Supramax Marketed Far East open 10days (S2) |
| S10 | Supramax Marketed South China open 10days (S10) |
| HS4 | Handy Marketed USG open 20 days (HS4) |
| HS5 | Handy Marketed SE Asia open 10 days (HS5) |

TC1 and TC5 are the Baltic routes that the LR2 and LR1 Arabian Gulf templates
match.

## Good to know

- **Relative windows.** A `*_relative_offset` range and `eta_relative_offset`
  count days from each snapshot day on `get_supply_trend` and
  `get_historical_supply`, and from today on `get_live_supply`. The templates
  use relative windows, so a template means the same on all three methods.
- **Commercial data history.** Commercial availability history starts on
  29 January 2026. For earlier days, the commercial filters and the ETA
  calculations use Signal's system-calculated values. Results before and
  after that day can look different.
- **Your organisation's data.** From your account's start date, results show
  your organisation's own positions and commercial data. Before that date,
  results come from Signal's baseline data.
- **Hub ports on the trend.** `get_supply_trend` always calculates ETAs to
  hub ports. An ETA basis port that is not a hub port is replaced by the hub
  port of its region, and the result's `notes` say so. So a trend count for an
  ETA template can differ a little from the live list of the same template.
  `get_historical_supply` uses the ports as given, unless you set
  `use_only_hub_ports=True`.
- **Daily limit on historical supply.** Each API key can call
  `get_historical_supply` 5 times per day. For counts over a date range, use
  `get_supply_trend`.
- **HS4.** Its name says 20 days, but its open window is 10 days. The SDK
  keeps the 10-day window of the template.
- **Errors.** When the API refuses a request, the SDK raises
  `requests.HTTPError`. The error message includes the API's explanation, for
  example which filter is not valid.

# Package Documentation

::: signal_ocean.supply
    handler: python
    rendering:
      show_source: false
