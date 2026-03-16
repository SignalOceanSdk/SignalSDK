# noqa: D100

from signal_ocean.util.pydantic_base import IdentityEqModel


class Port(IdentityEqModel):
    """A maritime facility where vessels can dock.

    Attributes:
        id: The ID of the port.
        name: The name of the port.
    """
    id: int
    name: str
