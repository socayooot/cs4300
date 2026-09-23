import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task4 import calculate_discount

#small number
price_1 = float(input("Please enter the first price (num < 10):  "))
#zero
price_2 = float(input("Please enter the second price (enter 0):  "))
#big number
price_3 = float(input("Please enter the third price (enter super big number):  "))
#float
price_4 = float(input("Please enter the fourth price (enter some decimal):  "))
#not a number
price_5 = input("Please enter the fifth price (enter a string):  ")
#test 100% discount
price_6 = float(input("Please enter the sixth price (use 100 for discount):  "))
#zero percent off
price_7 = float(input("Please enter a seventh price(enter 0 for the discount):  "))

small_test = calculate_discount(price_1)
print(small_test)
zero_test = calculate_discount(price_2)
print(zero_test)
big_test = calculate_discount(price_3)
print(big_test)
float_test = calculate_discount(price_4)
print(float_test)
string_test = calculate_discount(price_5)
print(string_test)
free_test = calculate_discount(price_6)
print(free_test)
no_discount_test = calculate_discount(price_7)
print(no_discount_test)