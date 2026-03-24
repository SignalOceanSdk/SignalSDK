# noqa: D100

import warnings
from typing import Any

from signal_ocean.util.pydantic_base import IdentityEqModel


class Port(IdentityEqModel):
    """A maritime facility where vessels can dock.

    Attributes:
        id: The ID of the port.
        name: The name of the port.
    """

    id: int
    name: str

    def model_post_init(self, __context: Any) -> None:
        """Initialize model."""
        warnings.warn(
            "signal_ocean.Port is deprecated and will be removed in a future "
            "version of the SDK. Please use tonnage_list.Port instead.",
            DeprecationWarning,
            stacklevel=3,
        )
