import random

import EuclidAlgorithm
import ExponentialTower
import Factorization
import PolynomialModularCongruence


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
    # print("Odd value is {}, exponent is {}".format(odd_m, exponent))
    new_value = ExponentialTower.create_exp_tower(base, odd_m)
    # print(new_value.show())
    prev_value = new_value.fast_exponentiation(number)
    if prev_value == 1:
        # print("{} is {}-pseudoprime due to first condition of MR test".format(number, base))
        return True
    else:
        count = 1
        while count < exponent + 1:
            new_value = ExponentialTower.create_exp_tower(base, odd_m * (2 ** count)).fast_exponentiation(number)
            # print("Prev_value is {}, new_value is {}".format(prev_value, new_value))
            if new_value == 1 and prev_value == number - 1:
                # print("{} is {}-pseudoprime due to second condition of MR test".format(number, base))
                return True
            else:
                prev_value = new_value
                count += 1
    # print("No condition has been satisfied. {} is not {}-pseudoprime".format(number, base))
    return False


def generate_a(number):
    a = 2
    while EuclidAlgorithm.get_gcd(a, number) != 1:
        a += 1
    return a


def generate_numbers_from(number, quantity):
    num_list = []
    a = 2
    for i in range(quantity):
        while EuclidAlgorithm.get_gcd(a, number) != 1:
            a += 1
        num_list.append(a)
        a += 1
    return num_list


def AKS_simple_criteria(number):
    constant = generate_a(number)
    left_polynome = PolynomialModularCongruence.generate_from_Newton([1, constant], number)
    # left_polynome.show()
    right_polynome = []
    for i in range(number + 1):
        if i == 0:
            right_polynome.append(1)
        elif i == number:
            right_polynome.append(constant)
        else:
            right_polynome.append(0)
    right_polynome = PolynomialModularCongruence.create_polynome(right_polynome, "x")
    right_polynome.modulate(number)
    # right_polynome.show()
    if left_polynome.equals(right_polynome, number):
        return True
    else:
        return False


def get_prime_factors(number, security_factor):
    values = generate_numbers_from(number, security_factor)
    for j in range(len(values)):
        # print("Miller_Rabin test for number {} and random {}".format(number, values[j]))
        if is_prime(number[j]):
            return [[number, 1]]
        else:
            factorization = []
            divisors = EuclidAlgorithm.get_divisors_of(number)
            for i in range(1, len(divisors)):
                if is_prime(divisors[i]):
                    counter = 1
                    temp_number = int(number / divisors[i])
                    while temp_number % divisors[i] == 0:
                        temp_number = int(temp_number / divisors[i])
                        counter += 1
                    factorization.append([divisors[i], counter])
            return factorization


def get_exponent_primes(number):
    exponents = []
    factorization = Factorization.Factorize(number)
    for i in range(len(factorization)):
        exponents.append(factorization[i][1])
    return exponents


def is_prime(number):
    assert number > 0
    if number < 3000:
        return AKS_simple_criteria(number)
    else:
        base = 2
        while EuclidAlgorithm.get_gcd(number, base) != 1:
            base += 1
        return Miller_Rabin_test(number, base)
