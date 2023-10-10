import math

import EuclidAlgorithm
import ExponentialTower

def get_odd_value_and_exponent(param):
    counter = 0
    while param % 2 == 0:
        counter += 1
        param = int(param / 2)
    else:
        return param, counter


def Miller_Rabin_test(number, base):
    assert EuclidAlgorithm.get_gcd(number, base) == 1
    odd_m, exponent = get_odd_value_and_exponent(number - 1)
    print("Odd value is {}, exponent is {}".format(odd_m, exponent))
    new_value = ExponentialTower.create_exp_tower(base, odd_m)
    print(new_value.show())
    prev_value = new_value.fast_exponentiation(number)
    if prev_value == 1:
        print("{} is {}-pseudoprime due to first condition of MR test".format(number, base))
        return True
    else:
        count = 1
        while count < exponent+1:
            new_value = ExponentialTower.create_exp_tower(base, odd_m * (2 ** count)).fast_exponentiation(number)
            print("Prev_value is {}, new_value is {}".format(prev_value, new_value))
            if new_value == 1 and prev_value == number-1:
                print("{} is {}-pseudoprime due to second condition of MR test".format(number, base))
                return True
            else:
                prev_value = new_value
                count += 1
    print("No condition has been satisfied. {} is not {}-pseudoprime".format(number, base))
    return False
