"""
This task demonstrates the use of numpy
"""
import numpy as np


def sort_array(arr):
    #Return a sorted copy of the given array.
    return np.sort(arr)


def find_min_max(arr):
    """Return a tuple of (minimum, maximum) values in the array."""
    return np.min(arr), np.max(arr)
