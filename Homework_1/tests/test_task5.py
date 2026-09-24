import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task5 import my_books, print_first_three, students, retrieve_student_name, retrieve_student_id

#test books
print_first_three(my_books)

#test name retrieval from dictionary
print("printing name")
retrieve_name_test = retrieve_student_name(students)
print("Here is the result: ", retrieve_name_test)

#test
print("printing student name")
retrieve_id_test = retrieve_student_id(students)
print("Here is the student id you're looking for:", retrieve_id_test)