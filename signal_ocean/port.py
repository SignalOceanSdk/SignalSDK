# noqa: D100

from dataclasses import dataclass
import warnings


@dataclass(frozen=True, eq=False)
class Port:
    """A maritime facility where vessels can dock.

    Attributes:
        id: The ID of the port.
        name: The name of the port.
    """

    id: int
    name: str

    def __post_init__(self) -> None:  # noqa: D105
        warnings.warn(
            "signal_ocean.Port is deprecated and will be removed in a future "
            "version of the SDK. Please use tonnage_list.Port instead.",
            DeprecationWarning,
            stacklevel=3,
        )
