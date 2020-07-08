from dataclasses import dataclass
from typing import Iterable

from .port import Port
from ._internals import contains_caseless


@dataclass(eq=False)
class PortFilter:
    name_like: str = None

    def _apply(self, ports: Iterable[Port]) -> Iterable[Port]:
        return filter(self.__does_port_match, ports)

    def __does_port_match(self, port: Port) -> bool:
        return not self.name_like or contains_caseless(self.name_like, port.name)
