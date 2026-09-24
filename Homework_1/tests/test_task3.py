# tests/test_task3.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from Task3 import check_sign, prime_num, sum_first_hundred


@pytest.mark.parametrize("num, expected", [
    (5, "positive"),
    (-5, "negative"),
    (0, "zero"),
])
def test_check_sign(num, expected):
    assert check_sign(num) == expected


def test_prime_num_first_ten():
    assert prime_num(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_sum_first_hundred():
    assert sum_first_hundred() == 5050