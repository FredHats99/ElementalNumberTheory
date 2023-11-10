import random

import DiofantineEquation
import EuclidAlgorithm
import ModularCongruence
import PrimalityTest


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
        for i in range(len(factorization)):
            if not base_factor.__contains__(factorization[i][0]):
                return False
        return True


def get_exponent_primes_smoothed(param, number, base_factor):
    alphas = PrimalityTest.get_exponent_primes(param, number)
    for i in range(len(alphas)):
        for j in range(len(base_factor)):
            pass
    pass


def initialization_step(modulo):
    smooth_class = Smooth_number(random.randint(3, 7))
    print("Smooth bound {} has been chosen".format(smooth_class.smooth_bound))
    counter = 0
    incrementer = 1
    matrix = []
    while counter <= 2 * smooth_class.BF_cardinality:
        if is_smooth(modulo + incrementer, smooth_class.smooth_bound):
            alphas = get_exponent_primes_smoothed(modulo + incrementer, 2, smooth_class.base_factor)
            print("{} is {}-smooth with exponents alpha = {}".format(modulo+incrementer, smooth_class.smooth_bound, alphas))
            v_check = ModularCongruence.normalize(modulo + incrementer, modulo)
            matrix_vector = []
            if is_smooth(v_check, 2):
                betas = []
                if v_check == 1:
                    for i in range(smooth_class.BF_cardinality):
                        betas.append(0)
                else:
                    betas = PrimalityTest.get_exponent_primes(v_check, 2)
                    print("{} (which is {} modulo {}) is {}-smooth with exponents {}".format(v_check, modulo+incrementer, modulo, smooth_class.smooth_bound, betas))
                    # create a row in gaussian matrix
                    for j in range(smooth_class.BF_cardinality):
                        matrix_vector.append(alphas[j] - betas[j])
                    matrix.append(matrix_vector)
                    counter += 1
        incrementer += 1
    return matrix
