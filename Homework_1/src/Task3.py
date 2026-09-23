"""
This task aims to create an if statement that checks if a given number is
positive, negative, or zero.

Additionally, creating a for loop that prints the first 10 prime numbers.

Finally, create a while loop that prints out the sum of all numbers from 1 
to 100.
"""

#check the sign of the number (a)
def check_sign(num):
    if (num > 0):
        return "positive"
    elif (num < 0):
        return "negative"
    elif (num == 0):
        return "zero"

def prime_num():
    count = 0
    num = 2

    #prints the first 10 prime numbers
    while count < 10:
        #assume its a prime number
        is_prime = True
        #check the see if the num from 2 to num is divisible by any number
        for i in range (2, num):
            #if found any divisibility, not a prime number
            if num % i == 0:
                is_prime = False
            
        if is_prime:
            print(num)
            count = count + 1
            
        num = num + 1

def sum_first_hundred():
    total = 0
    count = 0
    
    while count < 101:
        total = total + count
        count = count + 1 

    print(total)


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
print(Here is the sum of the first 100 numbers)
result = sum_first_hundred()
print(result)
# --------------------------------- end c -----------------------------------