from dataclasses import dataclass
from datetime import datetime
from typing import Union, Type, List, Optional

import pytest

from signal_ocean.util import parsing_helpers


@pytest.mark.parametrize("cap_words, snake_cased",
                         [('VesselTypeID', 'vessel_type_id'),
                          ('Flag', 'flag'),
                          ('Id', 'id'),
                          ('VesselName', 'vessel_name'), ('IMO', 'imo'),
                          ('teU14', 'te_u14')])
def test_to_snake_case(cap_words: str, snake_cased: str) -> None:
    transformed = parsing_helpers._to_snake_case(cap_words)
    assert transformed == snake_cased


@pytest.mark.parametrize("value, cls, expected",
                         [(None, type(None), None),
                          ('Abc', str, 'Abc'),
                          (1, int, 1),
                          ("1", int, 1),
                          (1, float, 1.),
                          (1., float, 1.),
                          ("1", float, 1.),
                          (1, bool, True),
                          (None, str, TypeError),
                          ('1909-07-01T00:00:00', datetime,
                           datetime(1909, 7, 1, 0, 0, 0)),
                          ([], list, NotImplementedError),
                          ('Abc', int, ValueError),
                          ('1909-17-01T00:00:00', datetime, ValueError)])
def test_parse_class(value: Union[str, int, float, bool, None],
                     cls: Type,
                     expected: Union[
                         str, int, float, bool, None, datetime, Type]) -> None:
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected):
            parsing_helpers._parse_class(value, cls)
    else:
        transformed = parsing_helpers._parse_class(value, cls)
        assert isinstance(transformed, cls)
        assert transformed == expected


@pytest.mark.parametrize("value, field_type, expected",
                         [(1, int, 1),
                          (1, Union[int, None], 1),
                          (None, Union[int, None], None),
                          (['a', 'b'], List, ['a', 'b']),
                          (['1', '2'], List, ['1', '2']),
                          (['1', '2'], List[int], [1, 2]),
                          (['1', '2'], Optional[List[int]], [1, 2]),
                          (['1', '2'], Optional[List], ['1', '2']),
                          (['1', '2'], Union[List[int], None], [1, 2]),
                          (['1', '2'], Union[List, None], ['1', '2']),
                          (['a', 'b'], List[int], ValueError),
                          (['a', 'b'], Optional[List[int]], ValueError)])
def test_parse_field(value: Union[str, int, float, bool, None],
                     field_type: Type,
                     expected: Union[
                         str, int, float, bool, None, datetime, Type]) -> None:
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected):
            parsing_helpers._parse_field(value, field_type)
    else:
        transformed = parsing_helpers._parse_field(value, field_type)
        assert type(transformed) == type(expected)
        assert transformed == expected


def test_parse_model():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_name: str
        model_score: float
        touched_by: str
        created_date: datetime
        version: int = None

    data = {'ModelID': 1, 'ModelName': 'model1', 'ModelScore': .97,
            'TouchedBy': 'signal',
            'CreatedDate': '2010-01-01T01:00:00'}

    parsed = parsing_helpers.parse_model(data, TestModel)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, model_name='model1',
                               model_score=.97,
                               touched_by='signal',
                               created_date=datetime(2010, 1, 1, 1, 0, 0))


def test_parse_model_rename_key():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_name: str

    data = {'ModelID': 1, 'NAME': 'model1'}
    rename_keys = {'NAME': 'model_name'}
    parsed = parsing_helpers.parse_model(data, TestModel, rename_keys)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, model_name='model1')


def test_parse_model_extra_attributes_are_ignored():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_name: str

    data = {'ModelID': 1, 'ModelName': 'model1', 'ModelScore': .97,
            'TouchedBy': 'signal', 'CreatedDate': '2010-01-01'}

    parsed = parsing_helpers.parse_model(data, TestModel)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, model_name='model1')


def test_parse_model_rename_key_extra_attribute_ignored():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int

    data = {'ModelID': 1}
    rename_keys = {'NAME': 'model_name'}
    parsed = parsing_helpers.parse_model(data, TestModel, rename_keys)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1)
