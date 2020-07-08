from datetime import datetime
from typing import Tuple
from dataclasses import dataclass

from .vessel import Vessel


@dataclass(frozen=True, eq=False)
class TonnageList:
    date: datetime
    vessels: Tuple[Vessel, ...]
