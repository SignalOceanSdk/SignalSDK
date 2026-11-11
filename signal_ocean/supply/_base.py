"""Base models for the Supply API, which uses camelCase JSON."""
from pydantic import BaseModel, ConfigDict


def _to_camel_case(name: str) -> str:
    """Convert a snake_case field name to the API's camelCase name."""
    first, *rest = name.split("_")
    return first + "".join(part.capitalize() for part in rest)


class SupplyRequestModel(BaseModel):
    """Base for request models; an unknown field name raises an error."""

    model_config = ConfigDict(
        alias_generator=_to_camel_case,
        populate_by_name=True,
        extra="forbid",
    )


class SupplyResponseModel(BaseModel):
    """Base for response models; unknown response fields are ignored."""

    model_config = ConfigDict(
        alias_generator=_to_camel_case,
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )
