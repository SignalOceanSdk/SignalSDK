# noqa: D100

from ..util.pydantic_base import SignalBaseModel


class Area(SignalBaseModel):
    """A geographical area.

    Attributes:
        name: The area name.
        location_taxonomy: The area's location taxonomy. See the
            LocationTaxonomy class for available values.
    """
    name: str
    location_taxonomy: str
