# v1.0.6
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Voyages API package
### Added horizon / latest_received_ais / predicted_ballast_distance / predicted_laden_distance fields
Four new fields exposed through the VoyageData API:

`horizon`: It can take "Historic", "Current" or "Future" values, depending on whether the voyage event is in the past (StartDate and EndDate both in the past), is current (StartDate in the past and EndDate in the future) \ or future (both StartDate and EndDate in the future). Note: the notions of "past", "current" and "future" are not derived by the current date, but by the comparison between the voyage dates and the latest received AIS for that specific vessel.

`latest_received_ais`: The most recent AIS update for the vessel. It is used to define the horizon of a voyage and its events.

`predicted_ballast_distance`: Computed distance of the ballast leg based on our distance model, in nautical miles. For current voyage, when vessel is ballast, it is the remaining distance between the vessel position and the first load port. For historical legs PredictedBallastDistance is empty.

`predicted_laden_distance`: Computed distance of the laden leg based on our distance model, in nautical miles. For current voyage, when vessel is laden, it is the remaining distance between the vessel position and the last discharge port. For historical legs PredictedLadenDistance is empty.


## Installation and Upgrade Notes
Update your package with:
`pip install signal-ocean -U`