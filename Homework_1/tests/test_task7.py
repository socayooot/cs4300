import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task7 import sort_array, find_min_max

#arrays
arr = np.array([2,4,5,6,7,1,0])
arr2 = np.array([989,12,3,6543234,76,9])

#testing sort
sort_arr = sort_array(arr)
print(*sort_arr)
sort_arr2 = sort_array(arr2)
print(*sort_arr2)

print()

#testing max
min_arr = find_min_max(arr)
print(min_arr)