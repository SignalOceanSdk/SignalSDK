# noqa: D100

from dataclasses import dataclass
from typing import Iterable, Optional
import warnings

from .vessel_class import VesselClass
from ._internals import contains_caseless


@dataclass(eq=False)
class VesselClassFilter:
    """A filter used to find specific vessel classes.

    Attributes:
        name_like: Used to find vessel classes by name. When specified, vessel
            classes whose names partially match (contain) the attribute's value
            will be returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def __post_init__(self) -> None:  # noqa: D105
        warnings.warn(
            "signal_ocean.VesselClassFilter is deprecated and will be removed "
            "in a future version of the SDK. Please use "
            "tonnage_list.VesselClassFilter with tonnage_list.TonnageListAPI "
            "instead.",
            DeprecationWarning,
            stacklevel=3,
        )

    def _apply(
        self, vessel_classes: Iterable[VesselClass]
    ) -> Iterable[VesselClass]:
        return filter(self.__does_class_match, vessel_classes)

    def __does_class_match(self, vessel_class: VesselClass) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, vessel_class.name
        )
