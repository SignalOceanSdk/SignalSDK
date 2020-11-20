# Historical Tonnage List

A HTL is a collection of Tonnage Lists, each of which has a timestamp and a collection of vessel data.

*[HTL]: Historical Tonnage List

More accurately, the vessel data consists of the following attributes:

| Attributes                       | Type        | Description                                             |
|----------------------------------|-------------|---------------------------------------------------------|
| ```imo```                        | int         | The vessel's IMO number.                                |
| ```name```                       | str         | The vessel's name.                                      |
| ```vessel_class```               | str         | The vessel's class name.                                |
| ```ice_class```                  | str         | The vessel's ice class.                                 |
| ```year_built```                 | int         | The year the vessel has been built.                     |
| ```deadweight```                 | int         | The vessel's deadweight.                                |
| ```length_overall```             | float       | The vessel's length overall.                            |
| ```breadth_extreme```            | int         | The vessel's breadth extreme.                           |
| ```subclass```                   | str         | The vessel's sub class.                                 |
| ```market_deployment```          | str         | Market deployment of the vessel.                        |
| ```push_type```                  | str         | Push type of the vessel.                                |
| ```open_port```                  | str         | The vessel's open port name.                            |
| ```open_date```                  | datetime    | The vessel's open date.                                 |
| ```operational_status```         | str         | Commercial status of the vessel.                        |
| ```commercial_operator```        | str         | The vessel's commercial operator.                       |
| ```commercial_status```          | str         | Operational status of the vessel.                       |
| ```eta```                        | datetime    | Estimated time of arrival.                              |
| ```latest_ais```                 | datetime    | Timestamp of the vessel's latest AIS information.       |
| ```open_prediction_accuracy```   | str         | How accurate is the open prediction.                    |
| ```open_areas```                 | Tuple[Area] | A hierarchical collection of areas the vessel opens at. |
| ```willing_to_switch_subclass``` | bool        | Is the vessel willing to switch its subclass            |
| ```availability_port_type```     | str         | Availability port type.                                 |
| ```availability_date_type```     | str         | Availability date type.                                 |

So, a Tonnage List comprises all the above vessel data with a point in time for a **Loading Port** and a **Vessel Class**.

Then, the Historical Tonnage Lists, consists of Tonnage Lists with a timestamp for each one (point in time), 
as many as the days in a time frame *(e.g last 90 days)*.

## The Historical Tonnage List in the Signal Ocean SDK

The Signal Ocean SDK covers a wide range of shipping data available in our **[The Signal Ocean Platform]("https://www.signalocean.com/platform")** 
with it's Python libraries, and the Historical Tonnage Lists library is on of them. 

SDK's user cannot only get data through this library, but also can filter them with built-in filters. This feature enables the user to focus only
to his targeted data, saving time from manual filtering and tens of lines of code.

A Historical Tonnage List can be retrieved via the ```HistoricalTonnageListAPI``` using the ```get_historical_tonnage_list``` function, with the following
parameters:

| Parameter name                                      | Description                                                                           |
|-----------------------------------------------------|---------------------------------------------------------------------------------------|
| ```loading_port``` <span style="color:red">*</span> | The loading port from which ETA will be calculated.                                   |
| ```vessel_class``` <span style="color:red">*</span> | The class of vessels to return.                                                       |
| ```laycan_end_in_days```                            | The maximum ETA expressed as a number of days after the end date.                     |
| ```start_date```                                    | The date of the earliest tonnage list in the response.                                |
| ```end_date```                                      | The date of the latest tonnage list in the response.                                  |
| ```time```                                          | Specifies the time of day for which the state of the tonnage lists will be retrieved. |
| ```vessel_filter```                                 | A filter defining which vessels should be included in the response.                   |

<span style="color:red">*Required</span>

and given a time-range, returns a Historical Tonnage List containing a Tonnage List for every day between the start and end dates, 
at the requested time of day.

If no input dates are provided, the last 10 days will be fetched (including today).

As described above, using the built-in filters can be very useful. This can be achieved using the ```VesselFilter``` and pass it to the optional parameter of 
the ```get_historical_tonnage_list```.

The ```VesselFilter``` enables vessel filtering in a Historical Tonnage List query and consists of the following attributes: 

| Attribute name                 | Description                                                                                                                                    |
|--------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| ```push_types```               | Return vessels with the specified push types. Use constants defined in the PushType class for the values of this attribute.                    |
| ```market_deployments```             | Return vessels with the specified market deployment types. Use constants defined in the MarketDeployment                                    |
| ```commercial_statuses```            | Return vessels with the specified commercial statuses. Use constants defined in the CommercialStatus                                        |
| ```vessel_subclass```                | Return vessels of the specified subclass. Use constants defined in the VesselSubclass class for the value of this attribute.                |
| ```add_willing_to_switch_subclass``` | When True, returns vessels that do not match the subclass but are willing to switch to it.                                                  |
| ```latest_ais_since```            | The maximum age, in days, of the vessel's AIS information at the time the tonnage list was captured.                                           |
| ```operational_statuses```        | Return vessels with the specified operational statuses. Use constants defined in the OperationalStatus class for the values of this attribute. |
| ```min_liquid_capacity```         | The minimum liquid capacity, in cubic meters, the vessel should be able to hold.                                                               |
| ```max_liquid_capacity```         | The maximum liquid capacity, in cubic meters, the vessel should be able to hold.                                                               |
| ```fixture_types```               | Return vessels with the specified fixture types. Use constants defined in the FixtureType class for the values of this attribute.              |
| ```last_cargo_types```            | Return vessels with the specified last cargo type IDs.                                                                                         |
| ```past_port_visits```            | Return vessels with the specified past port visits.                                                                                            |
| ```open_port_ids```               | Return vessels with the specified open port ids.                                                                                               |
| ```canakkale_cancelling```        | Return vessels with the specified Canakkale cancelling date.                                                                                   |
| ```open_date```                   | Return vessels with the specified open date.                                                                                                   |
| ```ice_classes```                 | Return vessels with the specified ice classes.                                                                                                 |
| ```min_cranes_ton_capacity```     | Return vessels with the specified minimum cranes ton capacity.                                                                                 |
| ```max_cranes_ton_capacity```     | Return vessels with the specified maximum cranes ton capacity.                                                                                 |
| ```min_length_overall```          | Return vessels with the specified minimum length overall.                                                                                      |
| ```max_length_overall```          | Return vessels with the specified maximum length overall.                                                                                      |
| ```min_breadth_extreme```         | Return vessels with the specified minimum breadth extreme.                                                                                     |
| ```max_breadth_extreme```         | Return vessels with the specified maximum breadth extreme.                                                                                     |
| ```openAreas```                   | Return vessels with the specified open area ids.                                                                                               |
| ```openCountries```               | Return vessels with the specified open country ids.                                                                                            |

All attributes in this class are optional, i.e. no filtering will be performed on attributes whose value is None.

Attributes that accept a list of values are used to perform an *OR* comparison. In other words, when a non-empty list of values is used, the Historical 
Tonnage List will contain vessels that match on **any** of the specified values. Using an empty list will result in no filtering at all.

!!! info
    The ```VesselFilter``` is mutable in order to allow making adjustments to existing instances if query results are unsatisfactory.

To get started with an example for the Historical Tonnage List please visit our [Tutorials for Historical Tonnage List](tutorials.md#historical-tonnagelist) section.