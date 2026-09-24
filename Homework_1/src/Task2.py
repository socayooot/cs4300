# src/Task2.py
"""
This task aims to showcase different variables and data types
"""

my_int = 12
my_float = 12.4
my_string = "meow"
my_boolean = True


def get_type_name(value):
    """Return the name of a value's type, e.g. 'int'."""
    return type(value).__name__