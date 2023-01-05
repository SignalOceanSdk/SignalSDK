# v2.0.1
Download here: [![PyPI version shields.io](https://img.shields.io/pypi/v/signal-ocean.svg)](https://pypi.python.org/pypi/signal-ocean/)

## Tonnage List API

- Add `open_port_id` property in the Vessel Class
- Add `commercial_operator_id` property in the Vessel Class
- Add `fixture_type` property in the Vessel Class
- Add `current_vessel_sub_type_id` property in the Vessel Class
- Add `current_vessel_sub_type` property in the Vessel Class
- Add `willing_to_switch_current_vessel_sub_type` property in the Vessel Class
- Add `id` property in the Area Class
- Add `taxonomy_id` property in the Area Class
- Updated: `geared` property type from `bool` to `Optional[bool]` in the Vessel Class
- Removed: `cranes_ton_capacity` from the Vessel Class
- Removed: `gear_details` from the Vessel Class

## Installation and Upgrade Notes
Update your package with: `pip install signal-ocean -U`