"""Helper functions for key name transformations."""
import functools
import re
from typing import Optional, Dict


_SNAKE_CASE_RE = re.compile('([a-z0-9])([A-Z])')


@functools.lru_cache(maxsize=512)
def _to_snake_case(s: str) -> str:
    """Transforms a string from CapWords to snake_case.

    Args:
        s: The string to transform

    Returns:
        The transformed string
    """
    return _SNAKE_CASE_RE.sub(r'\1_\2', s).lower()


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
