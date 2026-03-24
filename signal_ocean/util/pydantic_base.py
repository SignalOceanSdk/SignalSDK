"""Shared Pydantic v2 base models for SignalSDK."""
from datetime import datetime
from typing import Any

from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict

from signal_ocean._internals import parse_datetime


_ACRONYMS = frozenset({'id', 'imo', 'coa', 'pit', 'tpc'})


def _to_pascal_case(field_name: str) -> str:
    """Convert snake_case field name to PascalCase alias.

    Matches the Signal API naming convention where known acronyms ('id',
    'imo', 'coa', 'pit', 'tpc') are uppercased entirely rather than just
    title-cased (e.g. vessel_class_id -> VesselClassID,
    vessel_type_id -> VesselTypeID, imo -> IMO).

    Note: 'ais' is NOT in the acronyms set because the API is inconsistent
    — some endpoints use 'AIS' (e.g. IsImpliedByAIS) while others use 'Ais'
    (e.g. LowAisDensity). Fields needing 'AIS' should use explicit
    validation_alias instead.
    """
    def _capitalize(word: str) -> str:
        if word.lower() in _ACRONYMS:
            return word.upper()
        return word.capitalize()

    return ''.join(_capitalize(word) for word in field_name.split('_'))


def _parse_datetime(value: Any) -> Any:
    """Parse a datetime value, passing through existing datetime objects."""
    if isinstance(value, datetime):
        return value
    return parse_datetime(value)


UTCDatetime = Annotated[datetime, BeforeValidator(_parse_datetime)]


class SignalBaseModel(BaseModel):
    """Base model for all SignalSDK API response models."""

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,  # accept both field name and alias
        extra='ignore',
        alias_generator=_to_pascal_case,
    )


class IdentityEqModel(SignalBaseModel):
    """Base for models that use identity-based equality (eq=False)."""

    __eq__ = object.__eq__
    __hash__ = object.__hash__
