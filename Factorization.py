import math
import random

import EuclidAlgorithm
import IndexComputeAlgorithm
import ModularCongruence
import PrimalityTest


def is_perfect_square(n):
    sqrt_n = math.isqrt(n)
    return sqrt_n * sqrt_n == n


def Fermat(num):
    x = math.ceil(math.sqrt(num))  # x_0
    d = x ** 2 - num  # d_o
    print("x_0 = {}, d_0 = {}".format(x, d))
    counter = 1
    while not is_perfect_square(d):
        print("{} is not a perfect square so...".format(d))
        d += 2 * x + 1
        x += 1
        print("x_{} = {}, d_{} = {}".format(counter, x, counter, d))
        counter += 1
    return x + math.isqrt(d), x - math.isqrt(d)


def get_absolute_residue(value, modulo):
    tmp = ModularCongruence.normalize(value, modulo)
    while tmp > modulo / 2:
        tmp -= modulo
    while tmp < -modulo / 2:
        tmp += modulo
    return tmp


def Legendre(num, bound):
    a_j = []
    smooth_bound = IndexComputeAlgorithm.Smooth_number(bound)
    mod2_fact = [0] * (1 + smooth_bound.BF_cardinality)
    fact_matrix = []  # contains all factorizations
    fact = []
    counter = math.ceil(int(math.sqrt(num / 2)))
    while len(a_j) <= 3 or mod2_fact != [0] * (1 + smooth_bound.BF_cardinality):
        # print("Counter == {}".format(counter))
        square_res = get_absolute_residue(counter ** 2, num)
        # print("square residue is {}".format(square_res))
        if square_res == -1:
            fact = [1] + ([0] * smooth_bound.BF_cardinality)
            for j in range(smooth_bound.BF_cardinality):
                mod2_fact[j] += fact[j]
            a_j.append(counter)
            # print("Fact is {}".format(fact))
            fact_matrix.append(fact)
        elif square_res < 0:
            if IndexComputeAlgorithm.is_smooth(-square_res, smooth_bound.smooth_bound):
                fact = [1] + IndexComputeAlgorithm.get_exponent_primes_smoothed(-square_res, 2,
                                                                                smooth_bound.base_factor)
                for j in range(smooth_bound.BF_cardinality):
                    mod2_fact[j] += fact[j]
                a_j.append(counter)
                # print("Fact is {}".format(fact))
                fact_matrix.append(fact)
        elif square_res == 1:
            fact = [0] + ([0] * smooth_bound.BF_cardinality)
            for j in range(smooth_bound.BF_cardinality):
                mod2_fact[j] += fact[j]
            a_j.append(counter)
            # print("Fact is {}".format(fact))
            fact_matrix.append(fact)
        else:
            if IndexComputeAlgorithm.is_smooth(square_res, smooth_bound.smooth_bound):
                fact = [0] + IndexComputeAlgorithm.get_exponent_primes_smoothed(square_res, 2, smooth_bound.base_factor)
                for j in range(smooth_bound.BF_cardinality):
                    mod2_fact[j] += fact[j]
                a_j.append(counter)
                # print("Fact is {}".format(fact))
                fact_matrix.append(fact)
        for i in range(len(mod2_fact)):
            mod2_fact[i] = mod2_fact[i] % 2
        # print("a_j = {}\nmod2_fact = {}".format(a_j, mod2_fact))
        counter += 1
    total_prod = 1
    for i in range(len(a_j)):
        total_prod *= a_j[i]
    total_prod = get_absolute_residue(total_prod, num)  # a**2 mod n
    # print("total_prod is {}".format(total_prod))
    # print("fact_matrix is {}".format(fact_matrix))
    b_value = 1
    for i in range(len(fact_matrix[0])):
        temp_value = 0
        for j in range(len(fact_matrix)):
            temp_value += fact_matrix[j][i]
        temp_value /= 2
        b_value *= int(get_absolute_residue(smooth_bound.absolute_base_factor[i] ** temp_value, num))
    b_value = get_absolute_residue(b_value, num)  # b**2 mod n
    # print("b_value is {}".format(b_value))
    if total_prod != b_value and total_prod != -b_value:
        print("A factor for {} is {}".format(num, EuclidAlgorithm.get_gcd(total_prod - b_value, num)))
        return EuclidAlgorithm.get_gcd(total_prod - b_value, num)
    else:
        # print("iteration failed since a_value and b_value are equal. Will retry incrementing the smooth number")
        return Legendre(num, bound + 1)


def Rho_Pollard(num, init_condition):
    x = 2
    a = init_condition
    y = x
    old_values = []
    while EuclidAlgorithm.get_gcd(x - y, num) == 1 or x == y:
        x = ModularCongruence.normalize((x ** 2) + a, num)
        if old_values.__contains__(x):
            print("Using f(x) = x**2 + a, with a = {} ends in a loop! Retrying with a different value..".format(a))
            return Rho_Pollard(num, init_condition+1)
        y = ModularCongruence.normalize((ModularCongruence.normalize((y ** 2) + a, num) ** 2) + a, num)
        old_values.append(x)
        print("New x is {}, new y is {}".format(x,y))
    if EuclidAlgorithm.get_gcd(x - y, num) == num:
        print("Got trivial solution..retry with different initial conditions")
    else:
        print("A factor for value {} is {}".format(num, EuclidAlgorithm.get_gcd(x - y, num)))
        return EuclidAlgorithm.get_gcd(x - y, num)


def Factorize(num):
    if num == 1:
        return []
    elif PrimalityTest.is_prime(num):
        return [num]
    else:
        init_condition = random.randint(3, 10)
        if num % 2 == 0:
            num = int(num/2)
            while num % 2 == 0:
                num = int(num/2)
            return [2] + Factorize(num)
        factor = Rho_Pollard(num, init_condition)
        return list(set(Factorize(factor) + Factorize(int(num/factor))))
