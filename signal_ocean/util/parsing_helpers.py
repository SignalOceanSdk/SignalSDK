"""Helper functions to instantiate model classes."""
import dataclasses
import re
from datetime import datetime
from typing import Union, Type, TypeVar, Any, Optional, Dict, Iterable, cast

from signal_ocean._internals import parse_datetime

TModel = TypeVar("TModel")
NoneType = type(None)
ParsableClass = Union[str, int, float, bool, None, datetime]


def _to_snake_case(s: str) -> str:
    """Transforms a string from CapWords to snake_case.

    Args:
        s: The string to transform

    Returns:
        The transformed string
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def _to_camel_case(s: str,
                   rename_keys: Optional[Dict[str, str]] = None) -> str:
    """Transforms a string from snake_case to camel_case.

    Args:
        s: The string to transform
        rename_keys: Key names to transform explicitly to the desired
            target string when the default output is not adequate.

    Returns:
        The transformed string
    """
    _to_camelcase = s.split('_')
    _to_camelcase = [word.capitalize() for word in _to_camelcase]
    result = ''.join(_to_camelcase)

    if rename_keys:
        if s in rename_keys:
            result = rename_keys[s]

    return result


def _parse_class(value: Any, cls: Type[ParsableClass]) \
        -> ParsableClass:
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
    """
    if value is None and cls is not NoneType:
        raise TypeError(f'Cannot parse None as {cls}')

    if cls is NoneType:
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
        return value if isinstance(value, datetime) \
            else parse_datetime(value)

    raise TypeError(f'Cannot parse value {value} as {cls}')


def parse_model(data: Union[Dict[str, Any], Iterable[Any], Any],
                cls: Union[Type[TModel], Type[Any]],
                rename_keys: Optional[Dict[str, str]] = None) \
        -> Union[TModel, Any]:
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
    if cls is not NoneType and dataclasses.is_dataclass(cls) \
            and isinstance(data, dict):
        if rename_keys:
            for k, r, in rename_keys.items():
                if k in data:
                    data[r] = data.pop(k)

        field_names = set(f.name for f in dataclasses.fields(cls))
        field_types = {f.name: f.type for f in dataclasses.fields(cls)}

        parsed_data: Dict[str, Any] = {}
        for key, value in data.items():
            key = _to_snake_case(key)
            if key in field_names:
                field_type = field_types[key]
                parsed_data[key] = parse_model(
                    value, field_type, rename_keys=rename_keys
                )

        args = []
        for f in dataclasses.fields(cls):
            if f.name in parsed_data:
                a = parsed_data[f.name]
            elif f.default is not dataclasses.MISSING:
                a = f.default
            else:
                fc = getattr(f, 'default_factory')
                if fc is not dataclasses.MISSING:
                    a = fc()
                else:
                    raise TypeError(f'Cannot initialize class {cls}. '
                                    f'Missing required parameter {f.name}')
            args.append(a)

        return cls(*args)

    field_type_origin = getattr(cls, '__origin__', None)

    if field_type_origin is Union:
        for candidate_cls in getattr(cls, '__args__', []):
            try:
                return parse_model(
                    data, candidate_cls, rename_keys=rename_keys
                )
            except (TypeError, ValueError, NotImplementedError):
                continue

        raise ValueError(f'Cannot parse value {data} as {cls}')

    if field_type_origin is list and isinstance(data, Iterable):
        list_field_type = getattr(cls, '__args__', [])[0]
        if type(list_field_type) is TypeVar:
            return list(data)
        return [parse_model(
            v, list_field_type, rename_keys=rename_keys
            ) for v in data
        ]

    if field_type_origin is tuple and isinstance(data, Iterable):
        tuple_field_types = getattr(cls, '__args__', [])

        if not tuple_field_types:
            return tuple(data)
        return tuple(
            parse_model(
                v, tuple_field_types[0], rename_keys=rename_keys
                ) for v in data
            )

    parsable_classes = tuple(getattr(ParsableClass, '__args__', []))
    if cls in parsable_classes:
        return _parse_class(data, cast(Type[ParsableClass], cls))

    raise NotImplementedError(f'Cannot parse data {data} as {cls}.')
