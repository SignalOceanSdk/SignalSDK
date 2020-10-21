from decimal import Decimal

from signal_ocean._internals import as_decimal


def test_handles_None():
    assert as_decimal(None) is None


def test_handles_empty_strings():
    assert as_decimal("") is None


def test_parses_strings():
    assert as_decimal("12.345") == Decimal("12.345")


def test_handles_0():
    assert as_decimal(0.0) == Decimal("0.0")


def test_converts_floats_to_decimals_exactly():
    dec = as_decimal(24.390015)

    # due to float imprecision, will be 24.39001599999...
    assert dec != Decimal(24.390015)

    # will be precisely 24.390015
    assert dec == Decimal("24.390015")
