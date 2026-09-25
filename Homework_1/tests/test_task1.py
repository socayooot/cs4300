import sys
import os

#allows me to get the file to import task1
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task1 import print_hello


def test_print_hello_outputs_hello_world(capsys):
    print_hello()
    #grabs the output
    captured = capsys.readouterr()
    #check and capture the output
    assert captured.out == "Hello, World!\n"