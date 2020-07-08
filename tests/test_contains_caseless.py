import pytest

from signal_ocean._internals import contains_caseless


@pytest.mark.parametrize(
    'target, pattern, expected',
    [
        (None, None, False),
        (None, '', False),
        ('', None, False),
        (None, 'abc', False),
        ('abc', None, False),
        ('', '', True),
        ('', 'abc', False),
        ('abc', '', True),
        ('abc', 'abc', True),
        ('abc', 'a', True),
        ('abc', 'ab', True),
        ('abc', 'bc', True),
        ('a b c', ' ', True),
        ('abc', 'ABC', True),
        ('ABC', 'abc', True),
        ('abc', 'B', True),
        ('abc', 'xyz', False),
        ('ß', 'ss', True)
    ])
def test_check_if_target_contains_pattern_regardless_of_case(
        target: str,
        pattern: str,
        expected: bool):
    assert contains_caseless(pattern, target) == expected
