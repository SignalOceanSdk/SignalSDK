# noqa: D100

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Country:
    """Represents a country.

    Attributes:
        id: The ID of the country.
        name: The name of the country.
        country_code: Alpha-2 codes used by the ISO 3166
            standard.
        country_code_numeric: UN codes used by the ISO 3166
            standard.
        country_code_iso3: Alpha-3 codes used by the ISO 3166
            standard.
    """

    id: int
    name: str
    country_code: str
    country_code_numeric: str
    country_code_iso3: str


@dataclass(frozen=True)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: ID of the port.
        country_id: ID of the country the port is in.
        area_id: ID of the area the port is in.
        name: Name of the port.
        latitude: Latitude of the port.
        longitude: Longitude of the port.
    """

    id: int
    country_id: int
    area_id: int
    name: str
    latitude: Decimal
    longitude: Decimal


@dataclass(frozen=True)
class Area:
    """A geographical area.

    Attributes:
        id: ID of the area.
        name: Name of the area.
        area_type_id: ID of the area type.
        parent_area_id: ID of this area's parent area. None if the area has no
            parent.
    """

    id: int
    name: str
    area_type_id: int
    parent_area_id: Optional[int]
