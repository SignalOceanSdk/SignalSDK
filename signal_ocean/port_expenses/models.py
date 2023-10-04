# noqa: D100

from dataclasses import dataclass


@dataclass(frozen=True)
class PortExpenses:
    """The fees for port's facilities and services.

    Attributes:
        port_id: Port ID
        towage: Towage
        port_dues: Port dues
        pilotage: Pilotage
        agency_fees: Agency fees
        other: Other
        suez_dues: Suez dues
        total_cost: Total cost
        miscellaneous_dues: Mischellaneous dues
        is_estimated: Flag for estimation
        canal_dues: Canal dues
        berth_dues: Berth dues
        lighthouse_dues: Lighthouse dues
        mooring_unmooring: Mooring-unmooring
        quay_dues: Quay dues
        anchorage_dues: Anchorage dues
    """

    port_id: int
    towage: int
    port_dues: int
    pilotage: int
    agency_fees: int
    other: int
    suez_dues: int
    total_cost: int
    miscellaneous_dues: int
    is_estimated: bool
    canal_dues: int
    berth_dues: int
    lighthouse_dues: int
    mooring_unmooring: int
    quay_dues: int
    anchorage_dues: int


@dataclass(frozen=True)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: ID of the port.
        name: Name of the port.
    """

    id: int
    name: str


@dataclass(frozen=True)
class VesselType:
    """A vessel type.

    Attributes:
        id: The vessel type id, e.g. 1 -> Tanker, 3 -> Dry, 4 -> Containers,
            5 -> LNG (Liquified Natural gas),
            6-> LPG (Liquified Petroleum Gas).
        name: The vessel type name, e.g. Tanker, Dry, Containers,
            LNG (Liquified Natural gas), LPG (Liquified Petroleum Gas).
    """

    id: int
    name: str
