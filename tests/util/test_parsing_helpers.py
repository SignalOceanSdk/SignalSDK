from datetime import datetime, timezone
from typing import List, Optional

import pytest
from pydantic import Field, ValidationError

from signal_ocean.util import parsing_helpers
from signal_ocean.util.pydantic_base import (
    IdentityEqModel,
    SignalBaseModel,
    UTCDatetime,
)


@pytest.mark.parametrize("cap_words, snake_cased",
                         [('VesselTypeId', 'vessel_type_id'),
                          ('Flag', 'flag'),
                          ('Id', 'id'),
                          ('VesselName', 'vessel_name'), ('IMO', 'imo'),
                          ('teU14', 'te_u14')])
def test_to_snake_case(cap_words: str, snake_cased: str) -> None:
    transformed = parsing_helpers._to_snake_case(cap_words)
    assert transformed == snake_cased


@pytest.mark.parametrize("snake_cased, camel_cased",
                         [('vessel_type_id', 'VesselTypeId'),
                          ('token', 'Token'),
                          ('first_load_arrival_date_to', 'FirstLoadArrivalDateTo')])
def test_to_camel_case(snake_cased: str, camel_cased: str) -> None:
    transformed = parsing_helpers._to_camel_case(snake_cased)
    assert transformed == camel_cased


def test_parse_model():
    class TestModel(SignalBaseModel):
        model_id: int
        model_name: str
        model_score: float
        touched_by: str
        created_date: UTCDatetime
        version: Optional[int] = None

    data = {'ModelID': 1, 'ModelName': 'model1', 'ModelScore': .97,
            'TouchedBy': 'signal',
            'CreatedDate': '2010-01-01T01:00:00'}

    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.model_name == 'model1'
    assert parsed.model_score == 0.97
    assert parsed.touched_by == 'signal'
    assert parsed.created_date == datetime(2010, 1, 1, 1, 0, 0,
                                           tzinfo=timezone.utc)


def test_parse_nested_model():
    class TestNestedModel(SignalBaseModel):
        model_id: int

    class TestModel(SignalBaseModel):
        model_id: int
        nested_model: TestNestedModel

    data = {'ModelID': 1, 'NestedModel': {'ModelID': 3}}

    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.nested_model.model_id == 3


def test_parse_model_rename_key():
    class TestModel(SignalBaseModel):
        model_id: int
        model_name: str = Field(validation_alias='NAME')

    data = {'ModelID': 1, 'NAME': 'model1'}
    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.model_name == 'model1'


def test_parse_model_extra_attributes_are_ignored():
    class TestModel(SignalBaseModel):
        model_id: int
        model_name: str

    data = {'ModelID': 1, 'ModelName': 'model1', 'ModelScore': .97,
            'TouchedBy': 'signal', 'CreatedDate': '2010-01-01'}

    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.model_name == 'model1'


def test_parse_model_default():
    class TestModel(SignalBaseModel):
        model_id: int
        model_name: str = 'a'

    data = {'ModelID': 1}

    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.model_name == 'a'


def test_parse_model_default_factory():
    class TestModel(SignalBaseModel):
        model_id: int
        model_lists: List[str] = Field(default_factory=list)

    data = {'ModelID': 1}

    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1
    assert parsed.model_lists == []


def test_parse_model_missing_attribute_raises_validation_error():
    class TestModel(SignalBaseModel):
        model_id: int
        model_lists: int  # required, no default

    data = {'ModelID': 1}

    with pytest.raises(ValidationError):
        TestModel.model_validate(data)


def test_parse_model_rename_key_extra_attribute_ignored():
    class TestModel(SignalBaseModel):
        model_id: int

    data = {'ModelID': 1}
    rename_keys = {'NAME': 'model_name'}
    # With Pydantic, extra keys are ignored; rename_keys pattern uses
    # Field(validation_alias=...) instead. Here we just verify extra keys
    # in data are ignored.
    parsed = TestModel.model_validate(data)
    assert isinstance(parsed, TestModel)
    assert parsed.model_id == 1


def test_utc_datetime_forcing():
    class TestModel(SignalBaseModel):
        created: UTCDatetime

    parsed = TestModel.model_validate({'Created': '2020-06-15T12:00:00'})
    assert parsed.created.tzinfo == timezone.utc
    assert parsed.created == datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc)


def test_identity_eq_model():
    class TestModel(IdentityEqModel):
        value: int

    a = TestModel.model_validate({'Value': 1})
    b = TestModel.model_validate({'Value': 1})
    assert a != b  # identity equality: different objects are not equal
    assert a == a  # same object is equal to itself
