# noqa: D100

from typing import Iterable, Optional

from pydantic import ConfigDict

from .vessel_type import VesselType
from .._internals import contains_caseless
from signal_ocean.util.pydantic_base import IdentityEqModel, _to_pascal_case


class VesselTypeFilter(IdentityEqModel):
    """A filter used to find specific vessel types.

    Attributes:
        name_like: Used to find vessel types by name. When specified, vessel
            types whose names partially match (contain) the attribute's value
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

    def _apply(
        self, vessel_types: Iterable[VesselType]
    ) -> Iterable[VesselType]:
        return filter(self.__does_type_match, vessel_types)

    def __does_type_match(self, vessel_type: VesselType) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, vessel_type.name
        )
