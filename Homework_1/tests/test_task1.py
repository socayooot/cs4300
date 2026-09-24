# tests/test_task1.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task1 import print_hello


def test_print_hello_outputs_hello_world(capsys):
    print_hello()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"