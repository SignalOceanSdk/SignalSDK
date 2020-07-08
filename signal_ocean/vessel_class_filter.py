from dataclasses import dataclass
from typing import Iterable

from .vessel_class import VesselClass
from ._internals import contains_caseless


@dataclass(eq=False)
class VesselClassFilter:
    name_like: str = None

    def _apply(self, vessel_classes: Iterable[VesselClass]) -> Iterable[VesselClass]:
        return filter(self.__does_class_match, vessel_classes)

    def __does_class_match(self, vessel_class: VesselClass) -> bool:
        return not self.name_like or contains_caseless(self.name_like, vessel_class.name)
