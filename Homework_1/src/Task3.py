# src/Task3.py
"""
Checks if a number is positive, negative, or zero; finds the first N
prime numbers; sums 1 to 100.
"""


def check_sign(num):
    """Return 'positive', 'negative', or 'zero'."""
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"


def prime_num(count_needed=10):
    """Return a list of the first `count_needed` prime numbers."""
    primes = []
    num = 2

    while len(primes) < count_needed:
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
        if is_prime:
            primes.append(num)
        num = num + 1

    return primes


def sum_first_hundred():
    """Return the sum of all integers from 1 to 100."""
    total = 0
    count = 0
    while count < 101:
        total = total + count
        count = count + 1
    return total


if __name__ == "__main__":
    print(check_sign(5), check_sign(-5), check_sign(0))
    print("First 10 primes:", prime_num())
    print("Sum 1-100:", sum_first_hundred())