# src/Task5.py
"""
A list of favorite books and a student database using a dictionary.
"""

my_books = [
    ("The Search for Treasure", "Geronimo Stiliton"),
    ("The Hobbit", "J.R.R Tolkein"),
    ("Harry Potter", "JK Rowling"),
    ("The Shining", "Stephen King"),
]

students = {
    "Jeremy Bestal": "001",
    "Nathan Balay": "002",
    "Chris Hemsworth": "003",
    "Yu Ji-min": "004",
    "Sun Tzu": "005",
}


def print_first_three(books):
    """Return the first three books, using slicing."""
    return books[:3]


def retrieve_student_name(student_dict, name):
    for key in student_dict.keys():
        if key == name:
            return key
    return "Not Found"


def retrieve_student_id(student_dict, name):
    for student_name, sid in student_dict.items():
        if student_name == name:
            return sid
    return "not found"