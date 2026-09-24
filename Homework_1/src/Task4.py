# src/Task4.py
"""
calculate_discount takes a price and a discount percentage (any
numeric type) and returns the discounted price, using duck typing --
no explicit type() checks. Python itself raises TypeError naturally
if something non-numeric is passed in.
"""


def calculate_discount(price, discount_percent):
    if price < 0:
        raise ValueError("price cannot be negative")
    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be between 0 and 100")

    discount_amount = price * (discount_percent / 100)
    return price - discount_amount