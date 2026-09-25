import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from Task6 import count_words_in_file

READ_ME_PATH = os.path.join(os.path.dirname(__file__), "..", "task6_read_me.txt")


def test_word_count_of_read_me_file():
    assert count_words_in_file(READ_ME_PATH) == 127


@pytest.mark.parametrize("content, expected_count", [
    ("", 0),
    ("hello world", 2),
    ("   extra   whitespace   here   ", 3),
])
def test_word_count_various_contents(tmp_path, content, expected_count):
    f = tmp_path / "sample.txt"
    f.write_text(content, encoding="utf-8")
    assert count_words_in_file(str(f)) == expected_count


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        count_words_in_file("nope.txt")