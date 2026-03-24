# noqa: D100

from signal_ocean.util.pydantic_base import IdentityEqModel


class VesselType(IdentityEqModel):
    """Type of vessel used for transport.

    Attributes:
        id: The vessel type ID.
        name: The vessel type name.
    """
    id: int
    name: str
