# noqa: D100

from typing import Any, Iterable, Optional
import warnings

from pydantic import ConfigDict

from .vessel_class import VesselClass
from ._internals import contains_caseless
from signal_ocean.util.pydantic_base import IdentityEqModel, _to_pascal_case


class VesselClassFilter(IdentityEqModel):
    """A filter used to find specific vessel classes.

    Attributes:
        name_like: Used to find vessel classes by name. When specified, vessel
            classes whose names partially match (contain) the attribute's value
            will be returned. Matching is case-insensitive.
    """

    model_config = ConfigDict(
        frozen=False,
        populate_by_name=True,
        extra='ignore',
        alias_generator=_to_pascal_case,
    )

    __eq__ = object.__eq__
    __hash__ = object.__hash__

    name_like: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:  # noqa: D105
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
