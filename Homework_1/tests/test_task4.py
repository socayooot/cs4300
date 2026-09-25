import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from Task4 import calculate_discount


def test_discount_with_integers():
    assert calculate_discount(100, 20) == 80.0


def test_discount_with_floats():
    assert calculate_discount(49.99, 10) == pytest.approx(44.991)


def test_zero_discount():
    assert calculate_discount(75, 0) == 75


def test_full_discount():
    assert calculate_discount(75, 100) == 0


def test_negative_price_raises():
    with pytest.raises(ValueError):
        calculate_discount(-10, 20)


@pytest.mark.parametrize("bad_discount", [-5, 150])
def test_discount_out_of_range_raises(bad_discount):
    with pytest.raises(ValueError):
        calculate_discount(100, bad_discount)


def test_non_numeric_raises_type_error():
    with pytest.raises(TypeError):
        calculate_discount("100", 10)