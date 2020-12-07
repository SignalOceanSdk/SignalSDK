# noqa: D100

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PortExpenses:
    """The fees for port's facilities and services.

    Attributes:
        port_id: Port ID
        port_canal: Port Canal
        towage: Towage
        berth: Berth
        port_dues: Port dues
        lighthouse: Lighthouse
        mooring: Mooring
        pilotage: Pilotage
        quay: Quay
        anchorage: Anchorage
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
        port_agents: Port agents
    """

    port_id: int
    port_canal: int
    towage: int
    berth: int
    port_dues: int
    lighthouse: int
    mooring: int
    pilotage: int
    quay: int
    anchorage: int
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
    port_agents: List[int]


@dataclass(frozen=True)
class CanalExpenses:
    """The fees for canal's facilities and services.

    Attributes:
        total_cost: The total cost for the use of the canal
    """

    total_cost: int
