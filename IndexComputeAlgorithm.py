import random

import DiofantineEquation
import DiscreteLogTheory
import EuclidAlgorithm
import GroupsTheory
import ModularCongruence
import PrimalityTest
import numpy as np


def get_primes_less_than(number):
    base_factor = []
    cycle_init = 2
    while cycle_init <= number:
        if PrimalityTest.AKS_simple_criteria(cycle_init):
            base_factor.append(cycle_init)
        cycle_init += 1
    return base_factor


class Smooth_number:
    def __init__(self, smoothness_bound):
        self.smooth_bound = smoothness_bound
        self.base_factor = get_primes_less_than(smoothness_bound)
        self.absolute_base_factor = [-1]+self.base_factor
        self.BF_cardinality = len(self.base_factor)


def is_smooth(number, smoothness_bound):
    if number == 1:
        return True
    else:
        factorization = PrimalityTest.get_prime_factors(number, 1)
        base_factor = Smooth_number(smoothness_bound).base_factor
        # print("Base factor -> {}, factorization -> {}".format(base_factor, factorization))
        temp_factorization = []
        for j in range(len(factorization)):
            temp_factorization.append(factorization[j][0])
        for i in range(len(factorization)):
            if not base_factor.__contains__(temp_factorization[i]):
                return False
        return True


def get_exponent_primes_smoothed(number, security_factor, base_factor):
    alphas = [0] * len(base_factor)
    primes = PrimalityTest.get_prime_factors(number, security_factor)
    for i in range(len(primes)):
        temp_base = primes[i][0]
        index = base_factor.index(temp_base)
        alphas[index] = primes[i][1]
    # print("alphas = {}, primes = {}".format(alphas, primes))
    return alphas


def initialization_step(modulo, smooth_bound):
    smooth_class = Smooth_number(smooth_bound)
    print("Smooth bound {} has been chosen".format(smooth_class.smooth_bound))
    counter = 0
    incrementer = 1
    matrix = []
    while counter <= smooth_class.BF_cardinality - 1:
        if is_smooth(modulo + incrementer, smooth_class.smooth_bound):
            alphas = get_exponent_primes_smoothed(modulo + incrementer, 2, smooth_class.base_factor)
            print("{} is {}-smooth with exponents alpha = {}".format(modulo + incrementer, smooth_class.smooth_bound,
                                                                     alphas))
            v_check = ModularCongruence.normalize(modulo + incrementer, modulo)
            matrix_vector = []
            if is_smooth(v_check, 2):
                betas = []
                if v_check == 1:
                    for i in range(smooth_class.BF_cardinality):
                        betas.append(0)
                else:
                    betas = get_exponent_primes_smoothed(v_check, 2, smooth_class.base_factor)
                    print("{} (which is {} modulo {}) is {}-smooth with exponents {}".format(v_check,
                                                                                             modulo + incrementer,
                                                                                             modulo,
                                                                                             smooth_class.smooth_bound,
                                                                                             betas))
                    # create a row in gaussian matrix
                    for j in range(smooth_class.BF_cardinality):
                        matrix_vector.append(alphas[j] - betas[j])
                    if not matrix.__contains__(matrix_vector):
                        matrix.append(matrix_vector)
                        counter += 1
        incrementer += 1
    print("Matrix A is {}".format(matrix))
    b_vector = [0] * len(matrix)
    print("Vector B is {}".format(b_vector))
    # b_vector = [modulo - 1] * len(matrix)
    b_vector = [0, 0, 0, 0]
    solution_vector = solve_matrix(matrix,
                                   b_vector,
                                   modulo - 1)  # This vector contains k-values for log(r)(a) = kx (mod p), where r is still arbitrary and a belongs to the base factor of the smooth-bound
    for i in range(len(solution_vector)):
        solution_vector[i] = int(solution_vector[i])
    print("K-valued solution_vector: {}".format(solution_vector))
    cyclic_group = GroupsTheory.Remainder_cyclic_group(modulo)
    for j in smooth_class.base_factor:
        for k in cyclic_group.primitive_roots:
            if j == k:
                index = smooth_class.base_factor.index(j)
                k_value = solution_vector[index]
                lambda_value = ModularCongruence.normalize(
                    GroupsTheory.Remainder_class(k_value, modulo).get_reciprocal().value, modulo - 1)
                for t in range(len(solution_vector)):
                    solution_vector[t] = ModularCongruence.normalize(lambda_value * solution_vector[t], modulo)
                print("Solution vector = {}, lambda_value = {}, j = {}".format(solution_vector, lambda_value,
                                                                               j))
                return solution_vector, j


def solve_matrix(matrix, val_vector, modulo):
    temp_vector = []
    for i in range(len(matrix[0])):
        coefficient = 0
        for j in range(len(matrix)):
            temp_product = 1
            for k in range(len(matrix[0])):
                if k == i and matrix[j][k] != 0:
                    temp_product *= GroupsTheory.Remainder_class(matrix[j][k], modulo).get_reciprocal()
                else:
                    temp_product *= matrix[j][k]
            coefficient += temp_product
        temp_vector.append(
            ModularCongruence.init_congruence(coefficient, "x_{}".format(i), val_vector[i], modulo).solve())
    return temp_vector


def compute_index(root, modulo, value):
    solution_vector, j = initialization_step(modulo, 9)
    bases = Smooth_number(9).base_factor
    exponents = [0] * len(bases)
    b = -1
    while not bases.__contains__(b):
        for i in range(len(bases)):
            exponents[i] = random.randint(0, 10)
        b = value
        for j in range(len(exponents)):
            b *= bases[j] ** exponents[j]
        b = ModularCongruence.normalize(b, modulo)
    bases.append(value)
    exponents.append(1)
    print("Using bases {} and exponents {}, a value of {} has been found modulo {}...".format(bases, exponents, b,
                                                                                              modulo))
    linear_eq_vector = []
    index_of_right_term = bases.index(b)
    for i in range(len(exponents) - 1):
        if i == index_of_right_term:
            linear_eq_vector.append(1 - exponents[i])
        else:
            linear_eq_vector.append(-exponents[i])
    print("linear_eq_vector = {}".format(linear_eq_vector))
    temp_log = ModularCongruence.normalize(np.dot(linear_eq_vector, solution_vector), modulo)
    print("The log(base {}){} modulo {} is {}".format(j, value, modulo, temp_log))
