# tests/test_task2.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from Task2 import my_int, my_float, my_string, my_boolean, get_type_name


@pytest.mark.parametrize("value, expected_type_name", [
    (my_int, "int"),
    (my_float, "float"),
    (my_string, "str"),
    (my_boolean, "bool"),
])
def test_variable_has_expected_type(value, expected_type_name):
    assert get_type_name(value) == expected_type_name