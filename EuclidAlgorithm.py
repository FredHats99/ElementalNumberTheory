import math

import Teacher


@Teacher.teach
def get_extended_gcd(a, b, print_steps):
    yield f"[get_extended_gcd]:  a = {a}, b = {b}"
    if b == 0:
        gcd_result = 1, 0, a
        return gcd_result
    yield f"[get_extended_gcd({a},{b})] Recursion, a --> {b}, b --> {a % b}"
    x1, y1, gcd = get_extended_gcd(b, a % b, print_steps, print_steps=print_steps)
    x = y1
    y = x1 - (a // b) * y1
    yield f"[get_extended_gcd({a},{b})] Recursion, x = {x}, y = {y}, gcd = {gcd}"

    return x, y, gcd


@Teacher.teach
def get_gcd(a, b):
    yield f"[get_gcd]:  a = {a}, b = {b}"

    while b != 0:
        yield f"Step: a % b, a = {a}, b = {b}"
        temp = a % b
        a, b = b, temp

    gcd_result = a
    yield f"GCD: {gcd_result}"
    return gcd_result


def get_multiple_gcd(values, print_steps):
    assert len(values) > 1
    a = values[0]
    b = values[1]
    temp_gcd = get_gcd(a, b, print_steps=print_steps)
    for i in range(2, len(values)):
        temp_gcd = get_gcd(temp_gcd, values[i], print_steps=print_steps)
    # print("[EuclidAlgorithm.py]: Request: get gcd from values {} solved with solution {}".format(values, temp_gcd))
    return temp_gcd


def get_co_primes_with(value):
    temp_list = []
    for i in range(1, value + 1):
        if get_gcd(i, value) != 1:
            temp_list.append(i)
    return temp_list


def get_divisors_of(value):
    temp_list = []
    for i in range(1, int(math.sqrt(value)) + 1):
        if value % i == 0:
            temp_list.append(i)
            if int(value / i) != i:
                temp_list.append(int(value / i))
    temp_list.sort()
    return temp_list


def get_base_and_exponent(value):
    divisors = get_divisors_of(value)
    base = divisors[1]
    for i in range(2, len(divisors)):
        if divisors[i] % base != 0:
            return 0, 0
    return base, len(divisors) - 1
