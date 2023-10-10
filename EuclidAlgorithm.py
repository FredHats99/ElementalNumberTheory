def get_extended_gcd(a, b):
    if b == 0:
        return 1, 0, a

    x1, y1, gcd = get_extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return x, y, gcd


def get_gcd(a, b):
    if b == 0:
        return a
    else:
        return get_gcd(b, a % b)


def get_multiple_gcd(values):
    assert len(values) > 1
    a = values[0]
    b = values[1]
    temp_gcd = get_gcd(a, b)
    for i in range(2, len(values)):
        temp_gcd = get_gcd(temp_gcd, values[i])
    return temp_gcd


