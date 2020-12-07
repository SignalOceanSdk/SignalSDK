# noqa: D100

from datetime import datetime
from typing import Tuple
from dataclasses import dataclass

from .vessel import Vessel


@dataclass(frozen=True, eq=False)
class TonnageList:
    """A tonnage list as it occurred at a certain point in time.

    Attributes:
        date: The date and time at which the tonnage list was captured.
        vessels: Vessels present in the tonnage list at the point in time
        and their availability information. for more details see Vessel class.
    """
    date: datetime
    vessels: Tuple[Vessel, ...]
