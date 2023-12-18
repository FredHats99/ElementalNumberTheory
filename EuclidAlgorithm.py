import math


def get_extended_gcd(a, b):
    # print("[EuclidAlgorithm.py]: Request to get extended gcd between values {}".format((a, b)))
    if b == 0:
        # print("[EuclidAlgorithm.py]: Request solved with solution {}".format(a))
        return 1, 0, a

    x1, y1, gcd = get_extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return x, y, gcd


def get_gcd(a, b):
    while True:
        if b == 0:
            # print(
            #      "[EuclidAlgorithm.py]: Request:\n get gcd between values {} solved with solution {}".format((a, b), a))
            return a
        temp = a % b
        a = b
        b = temp


def get_multiple_gcd(values):
    assert len(values) > 1
    a = values[0]
    b = values[1]
    temp_gcd = get_gcd(a, b)
    for i in range(2, len(values)):
        temp_gcd = get_gcd(temp_gcd, values[i])
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
