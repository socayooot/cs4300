"""
Inside this task will be a list of my favorite books and a student database
using a dictionary
"""

#list of books 
my_books = [
    ("The Search for Treasure", "Geronimo Stiliton"),
    ("The Hobbit", "J.R.R Tolkein"),
    ("Harry Potter", "JK Rowling"),
    ("The Shining", "Stephen King")
]

#dictionary of students
students = {
    "Jeremy Bestal": "001",
    "Nathan Balay": "002",
    "Chris Hemsworth": "003",
    "Yu Ji-min": "004",
    "Sun Tzu": "005"
}

def print_first_three(list):
    print(list[:3])

def retrieve_student_name(dict):
    name = input("Enter the student you're looking for:  ").strip()
    print(name)

    for key in dict.keys():
        if key == name:
            return key

    return "Not Found"



