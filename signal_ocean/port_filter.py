# noqa: D100

from typing import Any, Iterable, Optional
import warnings

from pydantic import ConfigDict

from .port import Port
from ._internals import contains_caseless
from signal_ocean.util.pydantic_base import IdentityEqModel, _to_pascal_case


class PortFilter(IdentityEqModel):
    """A filter used to find specific ports.

    Attributes:
        name_like: Used to find ports by name. When specified, ports whose
            names partially match (contain) the attribute's value will be
            returned. Matching is case-insensitive.
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

    def model_post_init(self, __context: Any) -> None:
        """Initialize model."""
        warnings.warn(
            "signal_ocean.PortFilter is deprecated and will be removed in a "
            "future version of the SDK. Please use tonnage_list.PortFilter "
            "with tonnage_list.TonnageListAPI instead.",
            DeprecationWarning,
            stacklevel=3,
        )

    def _apply(self, ports: Iterable[Port]) -> Iterable[Port]:
        return filter(self.__does_port_match, ports)

    def __does_port_match(self, port: Port) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, port.name
        )
