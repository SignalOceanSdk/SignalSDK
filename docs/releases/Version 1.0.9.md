# v1.0.9
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Added Port Congestion package

One derivative of the voyages data is the calculation of various metrics regarding Port Congestion. We have added a new package that retrieves voyages data from  
Signal's Voyages Data API and calculates the following:  
- Number of vessels in ports/areas of interest over time   
- Waiting time of vessels in ports/areas of interest over time  
- Live Port Congestion in ports/areas of interest  


## Added get_port_congestion method
Method to retrive congestion data. It returns the following:

`VesselsCongestionData`: A DataFrame that stems from preprocessing the voyages data. It is used as a basis dataset, which is then manipulated to calculate the congestion.

`NumberOfVesselsOverTime`: DataFrame that holds information about the number of vessels at port point in time.

`WaitingTimeOverTime`: DataFrame that holds information about the average waiting time of vessels at port point in time.

`LiveCongestion`: DataFrame that describes the current situation regarding waiting and operatin vessels.

## Notebook examples update

### Port_Congestion_in_China_(Capes)
Updated the notebook to consume the Port Congestion Package

## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`