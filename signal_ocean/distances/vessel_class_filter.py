# noqa: D100

from dataclasses import dataclass
from typing import Iterable, Optional

from .vessel_class import VesselClass
from .._internals import contains_caseless


@dataclass(eq=False)
class VesselClassFilter:
    """A filter used to find specific vessel classes.

    Attributes:
        name_like: Used to find vessel classes by name. When specified, vessel
            classes whose names partially match (contain) the attribute's value
            will be returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def _apply(
        self, vessel_classes: Iterable[VesselClass]
    ) -> Iterable[VesselClass]:
        return filter(self.__does_class_match, vessel_classes)

    def __does_class_match(self, vessel_class: VesselClass) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, vessel_class.name
        )
