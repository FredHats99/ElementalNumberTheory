import cProfile
import random
import re
import time

import DiscreteLogTheory
import EuclidAlgorithm
import DiofantineEquation
import ExponentialTower
import Factorization
import IndexComputeAlgorithm
import ModularCongruence
import GroupsTheory
import PolynomialModularCongruence
import PrimalityTest
import QuadraticResidues
import QuadraticSieve
import RandNumbers
import Teacher


def main():
    # Test section, here is what about Elemental Number Theory can be done so far...

    # Calculate the gcd between two values (see EuclidAlgorithm.py)
    # x = EuclidAlgorithm.get_gcd(58, 24, print_steps=False)
    # print(x)
    # Solve diofantine equation of the form ax+by=c
    # x = DiofantineEquation.create_equation(["x", "y"], [5, -17], 6).solve(True)

    # Solve modular-arithmetic equations like: ax == b (mod n)
    # x = ModularCongruence.init_congruence(4, "x", 7, 17).solve(True)
    # x = ModularCongruence.init_system_of_congruences([[3, 1, 2], [2, 9, 7], [11, 0, 3]]).general_solve()

    # Find the remainder of arbitrarily big exponential towers
    x = ExponentialTower.create_exp_tower(6, ExponentialTower.create_exp_tower(3, ExponentialTower.create_exp_tower(4,
                                                                                                                    5))).fast_exponentiation(
        7)

    # Work with groups, finding the reciprocal subset and Euler value
    # x = GroupsTheory.Remainder_group(56).info
    # print(x)

    # Solve modular-arithmetic polynomial equations
    # print(PolynomialModularCongruence.create_polynome([12, 7, 19], "x").modulate(6))

    # Use AKS criteria to compute fast if a number is prime or not
    # print(PrimalityTest.is_prime(997))

    # Use Miller-Rabin test to compute even faster if a number is probably prime or not (pseudoprime in a certain base)
    # print(PrimalityTest.Miller_Rabin_test(279313, 2))

    # Work with cyclic groups generated from primes to get the primitive roots
    # x = GroupsTheory.Remainder_cyclic_group(17).info
    # print(x)

    # a = GroupsTheory.Remainder_set_cyclic_group(25)
    # a.generate_remainder_classes()
    # for i in range(len(a.remainder_classes)):
    # print(a.remainder_classes[i].value)

    # here i'm trying to work on an implementation of discrete logarithm problem solver, here is the first algorithm I came up with...
    # print(DiscreteLogTheory.DiscreteLog(23, 7, 6).solve_first_mode())
    # While this is a faster version of it
    # randNumber = RandNumbers.generate_random_prime(20)
    # start_time = time.time()
    # print(DiscreteLogTheory.DiscreteLog(randNumber, GroupsTheory.Remainder_cyclic_group(randNumber).generator, random.randint(2, randNumber)).cappellini_v3())
    # end_time = time.time()
    # print("Execution time: {}".format(end_time - start_time))

    # print(DiscreteLogTheory.DiscreteLog(1009, 11, 891).solve_with_hellman_pohlig())

    # start_time = time.time()
    # print(DiscreteLogTheory.DiscreteLog(13, 128, 207518).solve_with_hellman_pohlig())
    # end_time = time.time()
    # print("Execution time for Hellman-Pohlig: {}".format(end_time-start_time))

    # -->
    # print(ExponentialTower.create_exp_tower(6, 11 ** 6).fast_exponentiation(11 ** 7))
    # print((16614632 * 9236508) % (11 ** 7))

    # start_time = time.time()
    # DiscreteLogTheory.DiscreteLog(1000003, 2, 207518).cappellini_v3()
    # end_time = time.time()
    # print("Execution time for my algorithm: {}".format(end_time - start_time))

    # print(PrimalityTest.get_prime_factors(35, 2))
    # print(IndexComputeAlgorithm.compute_index(11, 31, 15))

    # print(Factorization.Factorize(8))
    # print(PrimalityTest.get_exponent_primes(8))
    # print(QuadraticResidues.LegendreSymbol(2, 13).calculate())

    # PrimalityTest.Fermat_number(4).is_Pepin_prime()
    # print(QuadraticResidues.get_square_root(3, RandNumbers.generate_random_prime(20)))
    # print(QuadraticResidues.Shanks_Tonelli(2, 5))
    # print(QuadraticResidues.sqrt(17, 32))
    # print(GroupsTheory.Remainder_cyclic_group(RandNumbers.generate_random_prime(16)).generator)

    # print(QuadraticSieve.get_sieves(1081, 10))
    # print(Factorization.Legendre(1081, 10))


main()
