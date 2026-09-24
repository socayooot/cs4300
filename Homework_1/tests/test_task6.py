import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task6 import count_words_in_file

path = os.path.join(os.path.dirname(__file__), "..", "task6_read_me.txt")

count_words = count_words_in_file(path)
print(count_words)