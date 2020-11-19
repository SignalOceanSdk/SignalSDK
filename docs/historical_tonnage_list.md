# Historical Tonnage List

A Historical Tonnage List (HTL) is a collection of Tonnage Lists, each of which has a timestamp and a collection of vessel data.

More accurately, the vessel data consists of the following parameters:

- IMO
- Vessel Class
- Ice Class
- Year Built
- Deadweight
- Length overall
- Breadth extreme
- Subclass
- Market deployment
- Push type
- Commercial operator
- Commercial status
- Estimated Time Arrival (ETA)
- Latest AIS
- Open prediction accuracy
- Open country
- Open narrow area
- Open wide area
- Availability port type
- Availability date type

So, a Tonnage List comprises all the above vessel data with a point in time for a **Loading Port** and a **Vessel Class**.

Then, the Historical Tonnage Lists, consists of Tonnage Lists with a timestamp for each one (point in time), 
as many as the days in a time frame *(e.g last 90 days)*.

## The Historical Tonnage List in the Signal Ocean SDK

The Signal Ocean SDK covers a wide range of shipping data available in our **[The Signal Ocean Platform]("https://www.signalocean.com/platform")** 
with it's Python libraries, and the Historical Tonnage Lists library is on of them. 

SDK's user cannot only get data through this library, but also can filter them with built-in filters. This feature enables the user to focus only
to his targeted data, saving time from manual filtering and tens of lines of code.