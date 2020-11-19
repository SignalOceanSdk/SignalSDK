# API Tutorials

Here you will find examples for each one of our APIs.

## Freight Pricing

The Freight pricing API retrieves freight prices for moving commodities between two port.

The following function is available:

```
get_freight_pricing
```

Args:

```
vessel_type: The type of vessel to calculate the prices for.
load_port: Port where the commodity is loaded.
discharge_port: Port where the commodity is discharged.
date: Date at which the freight price is requested.
vessel_subclass: The vessel's subclass.
```

Returns:

A collection of freight pricing items, one per vessel class.

### Moving commodity from Fujairah towards Singapore Example

The following example will display how to calculate the available freight prices to move a commodity from Fujairah to Singapore. We will use also the PortAPI to map ports to the Signal Geo schema.

```
from signal_ocean import Connection
connection = Connection(api_key=signal_ocean_api_key)
```

#### Call the freight pricing API

```
from signal_ocean.freight_pricing import FreightPricingAPI, VesselTypeFilter, VesselClassFilter, PortFilter, VesselType, VesselSubclass
from datetime import date

freight_pricing_api = FreightPricingAPI(connection)

vessel_type = freight_pricing_api.get_vessel_types(VesselTypeFilter(name_like='tanker'))[0]
load_port = freight_pricing_api.get_ports(PortFilter(name_like='Fujairah'))[0]
discharge_port = freight_pricing_api.get_ports(PortFilter(name_like='Singapore'))[0]

today = date.today()

freight_pricing = freight_pricing_api.get_freight_pricing(
    vessel_type,
    load_port=load_port, 
    discharge_port=discharge_port,
    date=today,
    vessel_subclass=VesselSubclass.DIRTY
)
```
#### Print out the result

Now we can hold the result and print it out on a dataframe

```
import pandas as pd

dataf = pd.DataFrame([{
    'vessel_class': p.vessel_class,
    'cargo_quantity': p.cargo_quantity,
    **p.costs.__dict__,
    **p.totals.__dict__ } for p in freight_pricing
])

dataf
```

|   | vessel_class | cargo_quantity | freight_rate | freight_cost | canal | total_cost | total_cost_per_ton |
|---|--------------|----------------|--------------|--------------|-------|------------|--------------------|
| 0 | VLCC         | 270000.0       | 3.90558      | 1054506.6    | 0.0   | 1054506.6  | 3.90558            |
| 1 | Suezmax      | 130000.0       | 5.402719     | 702353.47    | 0.0   | 702353.47  | 5.402719           |
| 2 | Aframax      | 80000.0        | 7.16023      | 572818.4     | 0.0   | 572818.4   | 7.16023            |

### Time Series Example

This example displays a use case of how we could use the Freight Pricing API in order to conduct a time series analysis regarding the freight rates. But first we should make sure that the Signal Ocean SDK is installed.

Set your subscription key acquired here: [Signal Ocean APIs Profile](https://apis.signalocean.com/profile)

```
signal_ocean_api_key = 'Not Valid' #replace with your subscription key
```
```
from signal_ocean import Connection
connection = Connection(api_key=signal_ocean_api_key)
```
```
from signal_ocean.freight_pricing import FreightPricingAPI
```
```
freight_pricing_api = FreightPricingAPI(connection)
```
We will use PortFilter module in order to set the loading and discharge port, as well as VesselTypeFilter to get the vessel type we want.
```
from signal_ocean.freight_pricing import FreightPricingAPI
from signal_ocean.freight_pricing import VesselTypeFilter, VesselClassFilter, PortFilter, VesselSubclass

load_port = freight_pricing_api.get_ports(PortFilter(name_like='Gamba'))[0]
discharge_port = freight_pricing_api.get_ports(PortFilter(name_like='Singapore'))[0]

vessel_type = freight_pricing_api.get_vessel_types(VesselTypeFilter(name_like='Tank'))[0]
```

```
from pandas import options
options.display.float_format = "{:,.2f}".format
```

#### Creating Time Series Data

Time Series data are created by calling the Freight Pricing API iteratively. Τime Window and Frequency are determined by first_day, last_day and weeks_before variables. In this specific example we will get the freight rates for every week for the last 52 weeks. Reference day is the present day of week.

```
import pandas as pd
import datetime as dt

last_day = dt.date.today() + pd.DateOffset(days= -1) #- pd.DateOffset(days= (- or +)...) To pick a specific date
weeks_before = 52 # here the number of weeks back can change
first_day = last_day + pd.DateOffset(days= -weeks_before*7)

df_dict = {}

for i in range(1,weeks_before+1):
    next_date = first_day + pd.DateOffset(days=i*7)
    freight_pricing_collection = freight_pricing_api.get_freight_pricing(
        vessel_type=vessel_type,
        load_port=load_port, 
        discharge_port=discharge_port,
        date=next_date,
        vessel_subclass=VesselSubclass.DIRTY)
    temp_dict = [o.__dict__ for o in freight_pricing_collection]
    for item in temp_dict:
        item['costs']= item['costs'].__dict__ 
        item['totals']= item['totals'].__dict__ 
    dataf = pd.json_normalize(data=temp_dict)
    fr_series = dataf['costs.freight_rate']
    df_dict[str(next_date)] = fr_series.values.tolist()
    
vessel_classes = dataf.vessel_class.tolist()
df_dict["vessel_class"] = vessel_classes
```
```
import numpy as np

data_types = {key:np.float for key in df_dict.keys()}
data_types["vessel_class"] = 'str'
```
```
final_df = pd.DataFrame.from_dict(df_dict).astype(data_types)
final_df
```

| 2019-11-06 00:00:00 | 2019-11-13 00:00:00 | 2019-11-20 00:00:00 | 2019-11-27 00:00:00 | 2019-12-04 00:00:00 | 2019-12-11 00:00:00 | 2019-12-18 00:00:00 | 2019-12-25 00:00:00 | 2020-01-01 00:00:00 | 2020-01-08 00:00:00 | ...   | 2020-09-02 00:00:00 | 2020-09-09 00:00:00 | 2020-09-16 00:00:00 | 2020-09-23 00:00:00 | 2020-09-30 00:00:00 | 2020-10-07 00:00:00 | 2020-10-14 00:00:00 | 2020-10-21 00:00:00 | 2020-10-28 00:00:00 | vessel_class |         |
|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|-------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|--------------|---------|
| 0                   | 22.11               | 18.89               | 20.38               | 26.72               | 23.26               | 24.64               | 23.72               | 27.06               | 35.78               | 30.83 | ...                 | 9.63                | 8.95                | 11.29               | 10.60               | 10.05               | 9.22                | 9.08                | 8.95                | 8.95         | VLCC    |
| 1                   | 26.95               | 21.99               | 29.02               | 30.52               | 29.59               | 34.09               | 32.93               | 38.69               | 49.00               | 42.80 | ...                 | 14.18               | 12.25               | 12.66               | 11.70               | 11.15               | 11.84               | 11.29               | 10.60               | 11.84        | Suezmax |
| 2                   | 25.68               | 25.68               | 46.98               | 47.56               | 47.56               | 42.95               | 49.29               | 50.44               | 64.41               | 58.22 | ...                 | 18.58               | 18.58               | 18.58               | 18.58               | 18.58               | 18.58               | 18.58               | 19.27               | 19.96        | Aframax |

Transposed dataframe is helpfull for the visualization of the data

```
final_df_transposed = final_df.set_index("vessel_class").T.rename_axis('Date')
final_df_transposed.head()
```
| vessel_class        | VLCC  | Suezmax | Aframax |
|---------------------|-------|---------|---------|
| Date                |       |         |         |
| 2019-11-06 00:00:00 | 22.11 | 26.95   | 25.68   |
| 2019-11-13 00:00:00 | 18.89 | 21.99   | 25.68   |
| 2019-11-20 00:00:00 | 20.38 | 29.02   | 46.98   |
| 2019-11-27 00:00:00 | 26.72 | 30.52   | 47.56   |
| 2019-12-04 00:00:00 | 23.26 | 29.59   | 47.56   |

```
# extracting the transposed ton an excel file
final_df.to_excel('simpleDemoFreightPricing.xlsx')
```

#### Visualizing the results in a graph
```
# creating x axis for the graph
variables_dict={}
for vc in  final_df.vessel_class.tolist():
    variables_dict["var%s" %vc] = final_df.loc[final_df.vessel_class==vc,str(first_day):str(last_day)].values.tolist()[0]

x_axis = final_df.loc[1:-1,str(first_day):str(last_day)].columns.tolist()
x_axis = [dt.datetime.strptime(x[0:10], '%Y-%m-%d') for x in x_axis]
```

```
#restrain the y axis
import numpy as np

minim = np.amin(final_df.loc[:,str(first_day):str(last_day)].values)
maxim = np.amax(final_df.loc[:,str(first_day):str(last_day)].values)
```

```
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)

ax.axes.set_ylim([minim - 1.5 ,maxim + 1.5])
ax.axes.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

for key,val in variables_dict.items():
    ax.plot(x_axis,val,label=key[3:])

plt.xticks(x_axis)

plt.xlabel("Dates", fontsize=15)
plt.ylabel("Total Rate ($/ton)", fontsize=15)

plt.legend(fontsize=20)

# format your data to desired format. Here I chose YYYY-MM-DD but you can set it to whatever you want.
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# rotate and align the tick labels so they look better
fig.autofmt_xdate()
```
![](image.png)

## Historical TonnageList

## Vessels

## Voyages

## Valuations

## Companies

## Distances