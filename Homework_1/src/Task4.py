"""
This task aims to showcase a function called "calculate_discount" and take in 
any integer or float and apply the discount.
"""

def calculate_discount(num):
    type_num = type(num)

    if type_num not in (int, float):
        print("not a proper input")
        return
    
    hold_num = num
    
    discount = float(input("please enter a discount: "))
    final_discount = discount / 100

    price_minus_discount = hold_num * final_discount
    final_price = hold_num - price_minus_discount
    return(final_price)
