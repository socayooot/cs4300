import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task5 import my_books, print_first_three, students, retrieve_student_name, retrieve_student_id


def test_print_first_three_books(capsys):
    print_first_three(my_books)
    captured = capsys.readouterr()
    assert captured.out == f"{my_books[:3]}\n"


def test_retrieve_student_name_found():
    assert retrieve_student_name(students, "Jeremy Bestal") == "Jeremy Bestal"


def test_retrieve_student_name_not_found():
    assert retrieve_student_name(students, "Nobody Here") == "Not Found"


def test_retrieve_student_id_found():
    assert retrieve_student_id(students, "Jeremy Bestal") == "001"


def test_retrieve_student_id_last_entry():
    # Regression test for the old indentation bug -- this used to
    # return "not found" for anyone who wasn't checked first.
    assert retrieve_student_id(students, "Sun Tzu") == "005"


def test_retrieve_student_id_not_found():
    assert retrieve_student_id(students, "Nobody Here") == "not found"