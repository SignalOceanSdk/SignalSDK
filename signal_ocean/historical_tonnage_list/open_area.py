from dataclasses import dataclass


@dataclass(frozen=True)
class OpenArea:
    name: str
    location_taxonomy: str
