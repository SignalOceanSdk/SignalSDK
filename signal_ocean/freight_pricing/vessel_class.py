# noqa: D100

from signal_ocean.util.pydantic_base import IdentityEqModel


class VesselClass(IdentityEqModel):
    """A group of vessels of similar characteristics.

    For example Aframax, Panamax, etc.

    Attributes:
        id: The vessel class ID.
        name: The vessel class name.
    """
    id: int
    name: str
