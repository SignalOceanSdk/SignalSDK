# v7.2.0
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

# Port Congestion API

- Update Port Congestion API response Models. Adds:
    - `QueueLoading`: The number of vessels in the queue with `Purpose = Loading`.
    - `QueueDischarging`: The number of vessels in the queue with `Purpose = Discharging`.
    - `AvgEventualDaysByDeparture`: Average number of total port days of all vessels departing on this date.

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`