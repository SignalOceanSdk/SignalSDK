# noqa: D100

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PortExpenses:
    """The fees for port's facilities and services.

    Attributes:
        port_id
        port_canal
        towage
        berth
        port_dues
        lighthouse
        mooring
        pilotage
        quay
        anchorage
        agency_fees
        other
        suez_dues
        total_cost
        miscellaneous_dues
        is_estimated
        canal_dues
        berth_dues
        lighthouse_dues
        mooring_unmooring
        quay_dues
        anchorage_dues
        port_agents
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
