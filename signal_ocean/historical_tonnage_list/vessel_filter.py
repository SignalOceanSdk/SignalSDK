from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Iterable, Union

from .vessel import Vessel
from .vessel_subclass import VesselSubclass


@dataclass(eq=False)
class VesselFilter:
    push_types: List[str] = field(default_factory=list)
    market_deployments: List[str] = field(default_factory=list)
    commercial_statuses: List[str] = field(default_factory=list)
    vessel_subclass: str = VesselSubclass.ALL
    add_willing_to_switch_subclass: bool = False
    latest_ais_since: int = None
    operational_statuses: List[str] = field(default_factory=list)

    def to_query_string(self) -> dict:
        return {
            'pushType': self.push_types,
            'commercialStatus': self.commercial_statuses,
            'latestAisSince': self.latest_ais_since,
            'vesselSubclass': self.vessel_subclass,
            'addWillingToSwitchSubclass': self.add_willing_to_switch_subclass,
            'marketDeployment': self.market_deployments,
            'operationalStatus': self.operational_statuses
        }
