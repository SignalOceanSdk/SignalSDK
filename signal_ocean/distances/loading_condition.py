# noqa: D100

from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class LoadingCondition:
    """The states of a vessel carrying cargo.

    Attributes:
        id: The loading condition ID.
        name: The loading condition name.
    """
    id: int
    name: str
