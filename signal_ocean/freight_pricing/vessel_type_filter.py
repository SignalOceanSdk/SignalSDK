# noqa: D100

from dataclasses import dataclass
from typing import Iterable, Optional

from .vessel_type import VesselType
from .._internals import contains_caseless


@dataclass(eq=False)
class VesselTypeFilter:
    """A filter used to find specific vessel types.

    Attributes:
        name_like: Used to find vessel types by name. When specified, vessel
            types whose names partially match (contain) the attribute's value
            will be returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def _apply(
        self, vessel_types: Iterable[VesselType]
    ) -> Iterable[VesselType]:
        return filter(self.__does_type_match, vessel_types)

    def __does_type_match(self, vessel_type: VesselType) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, vessel_type.name
        )
