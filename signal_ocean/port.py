from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Port:
    id: int
    name: str
