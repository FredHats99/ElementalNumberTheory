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
        self.BF_cardinality = len(self.base_factor)


def is_smooth(number, smoothness_bound):
    if number == 1:
        return True
    else:
        factorization = PrimalityTest.get_prime_factors(number, 1)
        base_factor = Smooth_number(smoothness_bound).base_factor
        print("Base factor -> {}, factorization -> {}".format(base_factor, factorization))
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
    print("alphas = {}, primes = {}".format(alphas, primes))
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
    b_vector = [modulo - 1] * len(matrix)
    return solve_matrix(matrix, b_vector)


def solve_matrix(matrix, val_vector):
    A = np.array(matrix)
    B = np.array(val_vector)
    return np.linalg.solve(A, B).tolist()


# def compute_index(root, modulo, value):

