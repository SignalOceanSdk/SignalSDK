from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Union, Type, List, Optional, Any, Tuple

import pytest

from signal_ocean.util import parsing_helpers


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

@pytest.mark.parametrize("value, cls, expected",
                         [(None, type(None), None),
                          ('Abc', str, 'Abc'),
                          (1, int, 1),
                          ("1", int, 1),
                          (1, float, 1.),
                          (1., float, 1.),
                          ("1", float, 1.),
                          (1, bool, True),
                          ('1909-07-01T00:00:00', datetime,
                           datetime(1909, 7, 1, 0, 0, 0,
                                    tzinfo=timezone.utc))])
def test_parse_class(value: Union[str, int, float, bool, None],
                     cls: Type,
                     expected: Union[str, int, float, bool, None, datetime]) \
        -> None:
    transformed = parsing_helpers._parse_class(value, cls)
    assert isinstance(transformed, cls)
    assert transformed == expected


@pytest.mark.parametrize("value, cls, expected_error",
                         [(None, str, TypeError),
                          ([], list, TypeError),
                          ('Abc', int, ValueError)])
def test_parse_class_raises_error(value: Union[str, int, float, bool, None],
                                  cls: Type,
                                  expected_error: Type[BaseException]) -> None:
    with pytest.raises(expected_error):
        parsing_helpers._parse_class(value, cls)


@pytest.mark.parametrize("value, field_type, expected",
                         [(1, int, 1),
                          (1, Union[int, None], 1),
                          (None, Union[int, None], None),
                          (['a', 'b'], List, ['a', 'b']),
                          (['1', '2'], List, ['1', '2']),
                          (['1', '2'], Tuple, ('1', '2')),
                          (['1', '2'], Tuple[int, ...], (1, 2)),
                          (['1', '2'], List[int], [1, 2]),
                          (['1', '2'], Optional[List[int]], [1, 2]),
                          (['1', '2'], Optional[List], ['1', '2']),
                          (['1', '2'], Union[List[int], None], [1, 2]),
                          (['1', '2'], Union[List, None], ['1', '2']),
                          (['1', '2'], Optional[Tuple[str, ...]], ('1', '2'))])
def test_parse_model_field(value: Union[str, int, float, bool, None],
                     field_type: Type,
                     expected: Union[str, int, float, bool, None, datetime,
                                     List[int], List[str], Tuple[int, ...],
                                     Tuple[str, ...]]) \
        -> None:
    transformed = parsing_helpers.parse_model(value, field_type)
    assert type(transformed) == type(expected)
    assert transformed == expected


@pytest.mark.parametrize("value, field_type, expected_error",
                         [(['a', 'b'], List[int], ValueError),
                          (['a', 'b'], Optional[List[int]], ValueError),
                          (1, Type[Any], NotImplementedError)])
def test_parse_model_field_raises_error(value: Union[str, int, float, bool, None],
                                  field_type: Type,
                                  expected_error: Type[BaseException]) -> None:
    with pytest.raises(expected_error):
        parsing_helpers.parse_model(value, field_type)


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
                               created_date=datetime(2010, 1, 1, 1, 0, 0,
                                                     tzinfo=timezone.utc))


def test_parse_nested_model():
    @dataclass(frozen=True)
    class TestNestedModel:
        model_id: int

    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        nested_model: TestNestedModel

    data = {'ModelID': 1, 'nested_model': {'ModelID': 3}}

    parsed = parsing_helpers.parse_model(data, TestModel)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, nested_model=TestNestedModel(3))


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


def test_parse_model_default():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_name: str = 'a'

    data = {'ModelID': 1}

    parsed = parsing_helpers.parse_model(data, TestModel)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, model_name='a')


def test_parse_model_default_factory():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_lists: List = field(default_factory=list)

    data = {'ModelID': 1}

    parsed = parsing_helpers.parse_model(data, TestModel)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1, model_lists=[])


def test_parse_model_missing_attribute_raises_type_error():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int
        model_lists: Any

    data = {'ModelID': 1}

    with pytest.raises(TypeError):
        parsing_helpers.parse_model(data, TestModel)


def test_parse_model_rename_key_extra_attribute_ignored():
    @dataclass(frozen=True)
    class TestModel:
        model_id: int

    data = {'ModelID': 1}
    rename_keys = {'NAME': 'model_name'}
    parsed = parsing_helpers.parse_model(data, TestModel, rename_keys)
    assert isinstance(parsed, TestModel)
    assert parsed == TestModel(model_id=1)
