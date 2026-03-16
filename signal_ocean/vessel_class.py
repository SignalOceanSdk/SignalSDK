# noqa: D100

import warnings
from typing import Any

from signal_ocean.util.pydantic_base import IdentityEqModel


class VesselClass(IdentityEqModel):
    """A group of vessels of similar characteristics.

    For example Aframax, Panamax, etc.

    Attributes:
        id: The vessel class ID.
        name: The vessel class name.
    """

    id: int
    name: str

    def model_post_init(self, __context: Any) -> None:
        """Initialize model."""
        warnings.warn(
            "signal_ocean.VesselClass is deprecated and will be removed in "
            "a future version of the SDK. Please use tonnage_list.VesselClass "
            "instead.",
            DeprecationWarning,
            stacklevel=3,
        )
