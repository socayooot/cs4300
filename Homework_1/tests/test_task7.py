import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task7 import sort_array, find_min_max


def test_sort_array():
    arr = np.array([2, 4, 5, 6, 7, 1, 0])
    assert np.array_equal(sort_array(arr), np.array([0, 1, 2, 4, 5, 6, 7]))


def test_find_min_max():
    arr = np.array([2, 4, 5, 6, 7, 1, 0])
    assert find_min_max(arr) == (0, 7)