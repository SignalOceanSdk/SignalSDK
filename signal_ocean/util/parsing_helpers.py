import dataclasses
import re
from datetime import datetime
from typing import Union, Type, TypeVar, Any, Optional, Dict

TModel = TypeVar("TModel")


def _to_snake_case(s: str) -> str:
    """Transforms a string from CapWords to snake_case.

    Args:
        s: The string to transform

    Returns:
        The transformed string
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def _parse_class(value: Union[str, int, float, bool, None], cls: Type) \
        -> Union[str, int, float, bool, None, datetime]:
    """Parses a value to match the type of a provided class.

    Args:
        value: The value to parse, can be str, int, float, bool or None.
        cls: The class type to parse the value to. Types of str, int, float,
            bool, NoneType and datetime are supported.

    Returns:
        The parsed object for the given value and class.

    Raises:
        TypeError: Cannot parse the value as the provided class.
        ValueError: Cannot parse the value as the provided class.
        NotImplementedError: The provided class is not supported.
    """
    none_type = type(None)
    if value is None and cls is not none_type:
        raise TypeError(f'Cannot parse None as {cls}')
    if cls is none_type:
        if value is not None:
            raise TypeError(f'Cannot parse {value} as NoneType')
        return None
    if cls is bool:
        return bool(value)
    if cls is int:
        return int(value)
    if cls is float:
        return float(value)
    if cls is str:
        return str(value)
    if cls is datetime:
        return datetime.fromisoformat(value[:19])

    raise NotImplementedError(f'Cannot parse value {value} as {cls}')


def _parse_field(value: Union[str, int, float, bool, None], field_type: Type) \
        -> Union[str, int, float, bool, None, datetime, list]:
    """Parses a value to match the type of a provided type.

    Identifies whether the provided type is a Union of different types or a
    specific type and tries to parse the value and create an object of one of
    the requested types.

    Args:
        value: The value to parse, can be str, int, float, bool or None.
        field_type: The type to parse the value to. Types of str, int, float,
            bool, NoneType and datetime, or Union of
            these types is supported.

    Returns:
        The parsed object for the given value and type.

    Raises:
        TypeError: Cannot parse the value as the provided class.
        NotImplementedError: The provided type is not supported.
    """
    field_type_origin = getattr(field_type, '__origin__', None)

    if field_type_origin is Union:
        for cls in getattr(field_type, '__args__', []):
            try:
                return _parse_field(value, cls)
            except (TypeError, ValueError):
                pass
        raise ValueError(f'Cannot parse value {value} as {field_type}')

    if field_type_origin is list:
        list_field_type = getattr(field_type, '__args__', [])[0]
        if isinstance(list_field_type, TypeVar):
            return list(value)
        return [_parse_field(v, list_field_type) for v in value]

    return _parse_class(value, field_type)


def parse_model(data: Dict[str, Any], cls: Type[TModel],
                rename_keys: Optional[Dict] = None) -> TModel:
    """Instantiates an object of the provided class cls for a provided mapping.

    Instantiates an object of a class specifying a model for the provided
    mapping. An entry in the mapping must be provided for all non-optional
    attribute of the class. Keys are expected to be in CapsWords, matching
    the snake_case corresponding class attributes. Any additional entries
    found in the mapping that do not correspond to class attributes are
    ignored.

    Args:
        data: Dictionary containing pairs with the names of the attributes
            and their respective values provided to instantiate the model
            class.
        cls: The model class to instantiate.
        rename_keys: Key names to rename to match model attribute names,
            used when an automated translation of the name from CapsWords
            to snake_case is to sufficient. Renaming must provide the name
            in CapsWords.

    Returns:
        The instantiated model class object.

    Raises:
        TypeError: Cannot parse the value of a class attribute to the
            appropriate type.
        NotImplementedError: The type of a class attribute is not supported.
    """
    if rename_keys:
        for k, r, in rename_keys.items():
            if k in data:
                data[r] = data.pop(k)

    fields = set(f.name for f in dataclasses.fields(cls))
    field_types = {f.name: f.type for f in dataclasses.fields(cls)}

    parsed_data = {}
    for key, value in data.items():
        key = _to_snake_case(key)
        if key in fields:
            field_type = field_types[key]
            parsed_data[key] = _parse_field(value, field_type)

    return cls(**parsed_data)
