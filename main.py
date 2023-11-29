import cProfile
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


def main():
    # Test section, here is what about Elemental Number Theory can be done so far...

    # Calculate the gcd between two values (see EuclidAlgorithm.py)
    # print(EuclidAlgorithm.get_gcd(1801, 63))

    # Solve diofantine equation of the form ax+by=c
    # print(DiofantineEquation.create_equation(["x", "y"], [5, -17], 6).solve())

    # Solve modular-arithmetic equations like: ax == b (mod n)
    # print(ModularCongruence.init_congruence(4, "x", 1, 17).solve())
    # print(ModularCongruence.init_system_of_congruences([[3, 0, 7], [2, 0, 7], [5, 0, 7]]).general_solve())

    # Find the remainder of arbitrarily big exponential towers
    # print(ExponentialTower.create_exp_tower(6, 9).fast_exponentiation(11))

    # Work with groups, finding the reciprocal subset and Euler value
    # GroupsTheory.Remainder_group(16).print()

    # Solve modular-arithmetic polynomial equations
    # print(PolynomialModularCongruence.create_polynome([12, 7, 19], "x").modulate(6))

    # Use AKS criteria to compute fast if a number is prime or not
    # print(PrimalityTest.is_prime(11))

    # Use Miller-Rabin test to compute even faster if a number is probably prime or not (pseudoprime in a certain base)
    # print(PrimalityTest.Miller_Rabin_test(279313, 2))

    # Work with cyclic groups generated from primes to get the primitive roots
    # GroupsTheory.Remainder_cyclic_group(1000037).print()

    # a = GroupsTheory.Remainder_set_cyclic_group(25)
    # a.generate_remainder_classes()
    # for i in range(len(a.remainder_classes)):
    # print(a.remainder_classes[i].value)

    # here i'm trying to work on an implementation of discrete logarithm problem solver, here is the first algorithm I came up with...
    # print(DiscreteLogTheory.DiscreteLog(23, 7, 6).solve_first_mode())
    # While this is a faster version of it
    # print(DiscreteLogTheory.DiscreteLog(1000003, 2, 207518).cappellini_v2())

    # print(DiscreteLogTheory.DiscreteLog(1009, 11, 891).solve_with_hellman_pohlig())

    # start_time = time.time()
    # print(DiscreteLogTheory.DiscreteLog(1000003, 2, 207518).solve_with_hellman_pohlig())
    # end_time = time.time()
    # print("Execution time for Hellman-Pohlig: {}".format(end_time-start_time))

    # -->
    # print(ExponentialTower.create_exp_tower(5, 9).fast_exponentiation(17))

    # start_time = time.time()
    # DiscreteLogTheory.DiscreteLog(1000003, 2, 207518).cappellini_v3()
    # end_time = time.time()
    # print("Execution time for my algorithm: {}".format(end_time - start_time))

    # print(PrimalityTest.get_prime_factors(35, 2))
    # print(IndexComputeAlgorithm.compute_index(11, 31, 15))

    # print(Factorization.Factorize(50))
    # print(PrimalityTest.get_exponent_primes(50))
    print(QuadraticResidues.LegendreSymbol(13, 19).calculate())


main()
