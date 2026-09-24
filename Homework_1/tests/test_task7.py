import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task7 import sort_array

arr = np.array([2,4,5,6,7,1,0])

new_arr = sort_array(arr)
print(new_arr)