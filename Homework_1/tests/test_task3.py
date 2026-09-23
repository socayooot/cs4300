import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from Task3 import check_sign, prime_num, sum_first_hundred

# ----------------------------------- a -------------------------------------
pos_num = int(input("Positive number test: "))
neg_num = int(input("Negative number test: "))
zer_num = int(input("zero number test: "))

pos_result = check_sign(pos_num)
neg_result = check_sign(neg_num)
zer_result = check_sign(zer_num)

print(pos_result)
print(neg_result)
print(zer_result)
# --------------------------------- end a -----------------------------------
print()
# ----------------------------------- b -------------------------------------
print("Here is a list of the first 10 prime numbers: ")
prime_num()
# --------------------------------- end b -----------------------------------
print()
# ----------------------------------- c -------------------------------------
print("Here is the sum of the first 100 numbers")
result = sum_first_hundred()
print(result)
# --------------------------------- end c -----------------------------------