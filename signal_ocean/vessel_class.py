from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class VesselClass:
    id: int
    name: str
