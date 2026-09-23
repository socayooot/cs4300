import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task2 import my_int, my_float, my_string, my_boolean

print("Here is the type of my_int", type(my_int))
print("Here is the type of my_float", type(my_float))
print("Here isd the type of my_string", type(my_string))
print("Here is the type of my_boolean", type(my_boolean))