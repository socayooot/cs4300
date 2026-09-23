import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task5 import my_books, print_first_three, students, retrieve_student_name

print_first_three(my_books)
result = retrieve_student_name(students)
print("Here is the result: ", result)