# noqa: D100

from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: The ID of the port.
        name: The name of the port.
    """
    id: int
    name: str
