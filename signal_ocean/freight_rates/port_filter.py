# noqa: D100

from dataclasses import dataclass
from typing import Iterable, Optional

from .models import Port
from .._internals import contains_caseless


@dataclass(eq=False)
class PortFilter:
    """A filter used to find specific ports.

    Attributes:
        name_like: Used to find ports by name. When specified, ports whose
            names partially match (contain) the attribute's value will be
            returned. Matching is case-insensitive.
    """

    name_like: Optional[str] = None

    def _apply(self, ports: Iterable[Port]) -> \
            Iterable[Port]:
        return filter(self.__does_port_match, ports)

    def __does_port_match(self, port: Port) -> bool:
        return not self.name_like or contains_caseless(
            self.name_like, port.name
        )
