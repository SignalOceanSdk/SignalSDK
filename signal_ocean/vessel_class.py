# noqa: D100

from dataclasses import dataclass
import warnings


@dataclass(frozen=True, eq=False)
class VesselClass:
    """A group of vessels of similar characteristics, i.e. Aframax, Panamax, etc.

    Attributes:
        id: The vessel class ID.
        name: The vessel class name.
    """

    id: int
    name: str

    def __post_init__(self) -> None:  # noqa: D105
        warnings.warn(
            "signal_ocean.VesselClass is deprecated and will be removed in "
            "a future version of the SDK. Please use tonnage_list.VesselClass "
            "instead.",
            DeprecationWarning,
            stacklevel=3,
        )
