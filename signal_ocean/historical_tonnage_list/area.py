# noqa: D100

from dataclasses import dataclass


@dataclass(frozen=True)
class Area:
    """A geographical area.

    Attributes:
        name: The area name.
        location_taxonomy: The area's location taxonomy. See the
            LocationTaxonomy class for available values.
    """
    name: str
    location_taxonomy: str
