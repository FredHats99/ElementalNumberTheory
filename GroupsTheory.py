import math

import ExponentialTower
import Factorization
import ModularCongruence
import EuclidAlgorithm
import PrimalityTest


class Remainder_class:
    def __init__(self, value, modulo):
        self.value = value
        self.mod = modulo

    def __add__(self, other):
        assert self.mod == other.mod
        return Remainder_class(ModularCongruence.normalize(self.value + other.value, self.mod), self.mod)

    def get_opposite(self):
        return Remainder_class(ModularCongruence.normalize(-self.value, self.mod), self.mod)

    def __mul__(self, other):
        assert self.mod == other.mod
        return Remainder_class(ModularCongruence.normalize(self.value * other.value, self.mod), self.mod)

    def raise_to(self, exponent):
        power = ExponentialTower.create_exp_tower(self.value, exponent)
        return Remainder_class(power.fast_exponentiation(self.mod), self.mod)

    def get_reciprocal(self):
        try:
            tmp = ModularCongruence.init_congruence(self.value, "x", 1, self.mod)
            tmp.solve()
            return Remainder_class(ModularCongruence.parse_fixed_value(tmp.solution), self.mod)
        except TypeError:
            print("Oops")
            return None


class Remainder_group:
    def __init__(self, modulo):
        self.mod = modulo
        self.remainder_classes = []
        self.reciprocal_subset = []
        # Remainder classes
        for i in range(self.mod):
            rem_class = Remainder_class(i, self.mod)
            self.remainder_classes.append(rem_class)
        # reciprocal subset
        for j in range(1, self.mod):
            value = self.remainder_classes[j].get_reciprocal()
            if value is not None:
                self.reciprocal_subset.append(self.remainder_classes[j].value)
        # Euler value
        self.euler_value = self.compute_Euler_value()
        self.info = self.info()

    def info(self):
        return "[GroupsTheory.py]:\nGroup modulo {} has:\nReciprocal classes: {},\nEuler value: {}".format(self.mod,
                                                                                                           self.reciprocal_subset,
                                                                                                           self.euler_value)

    def compute_Euler_value(self):
        temp_Euler_value = self.mod
        remainder_values = []
        for j in range(len(self.remainder_classes)):
            if self.remainder_classes[j].value != 0:
                remainder_values.append(self.remainder_classes[j].value)
        print(remainder_values)
        prime_divisors = Factorization.Factorize(self.mod)
        for i in range(len(prime_divisors)):
            temp_Euler_value *= (1 - 1 / prime_divisors[i])
        return int(temp_Euler_value)


def get_prime_divisors_of(subset, param):
    prime_divisors = []
    for i in range(len(subset)):
        if EuclidAlgorithm.get_gcd(subset[i], param) != 1 and PrimalityTest.is_prime(subset[i]):
            prime_divisors.append(subset[i])
    return prime_divisors


def isCyclic(number):
    if number == 1:
        return True, 1, 1
    elif number == 2:
        return True, 2, 1
    elif number == 4:
        return True, 2, 2
    else:
        if number % 2 == 0:
            base, exponent = EuclidAlgorithm.get_base_and_exponent(int(number / 2))
            if (base, exponent) != (0, 0) and base != 2:
                return True, [2, base], [1, exponent]
        else:
            base, exponent = EuclidAlgorithm.get_base_and_exponent(number)
            if (base, exponent) != (0, 0) and base != 2:
                return True, base, exponent
        return False, 0, 0


class Remainder_cyclic_group(Remainder_group):
    def __init__(self, modulo):
        self.generator = 1
        self.primitive_roots = []
        self.isCyclic, self.base, self.exponent = isCyclic(modulo)
        if self.isCyclic:
            super().__init__(modulo)
            if (self.base, self.exponent) == (2, 1):
                self.generator = 1
                self.primitive_roots = [1]
            else:
                # Get a generator
                if self.exponent != 1 or type(self.exponent) == list:
                    self.get_non_trivial_generator()
                    self.get_non_trivial_primitive_roots()
                else:
                    prime_divisors = get_prime_divisors_of(self.reciprocal_subset, self.euler_value)
                    for i in range(1, len(self.remainder_classes)):
                        for j in range(len(prime_divisors)):
                            if ExponentialTower.create_exp_tower(self.remainder_classes[i].value,
                                                                 int(self.mod / prime_divisors[j])).fast_exponentiation(self.mod) == 1:
                                break
                            if j == len(prime_divisors) - 1:
                                self.generator = self.remainder_classes[i].value
                    # Get primitive roots
                    for i in range(1, len(self.remainder_classes)):
                        for j in range(len(prime_divisors)):
                            if self.exponent != 1:
                                if ExponentialTower.create_exp_tower(self.remainder_classes[i].value,
                                                                     int(self.mod / prime_divisors[
                                                                         j])).fast_exponentiation(self.base) == 0:
                                    break
                            else:
                                if ExponentialTower.create_exp_tower(self.remainder_classes[i].value,
                                                                     int(self.mod / prime_divisors[
                                                                         j])).fast_exponentiation(self.mod) == 1:
                                    break
                            if j == len(prime_divisors) - 1:
                                self.primitive_roots.append(self.remainder_classes[i].value)
        else:
            raise Exception("This modulo does not allow a cyclic group\nIn fact contains the factor {}".format(
                Factorization.Factorize(modulo)))
        self.info = self.print()

    def print(self):
        return "[GroupsTheory.py]: Cyclic group modulo {} has:\nEuler value: {}\nGenerator: {}\nPrimitive roots: {}".format(
            self.mod,
            self.euler_value,
            self.generator,
            self.primitive_roots)

    def compute_Euler_value(self):
        if type(self.base) == list:
            temp = self.mod
            for i in range(len(self.base)):
                temp *= int(1 - 1 / self.base[i])
            return temp
        else:
            return int(self.mod * (1 - 1 / self.base))

    def get_non_trivial_generator(self):
        if type(self.base) != list:
            base_remainder_class_generator = Remainder_cyclic_group(self.base).generator
            kernel_generator = self.base + 1
            self.generator = ModularCongruence.normalize(base_remainder_class_generator * kernel_generator, self.base)
        else:
            base_remainder_class_generator = 1
            kernel_generator = self.base[1] + 1
            self.generator = ModularCongruence.normalize(base_remainder_class_generator + kernel_generator, self.mod)

    def get_non_trivial_primitive_roots(self):
        if type(self.base) == list:
            self.primitive_roots.append(self.generator)
            for i in range(2, self.euler_value):
                if EuclidAlgorithm.get_gcd(i, self.euler_value) == 1:
                    self.primitive_roots.append(
                        ExponentialTower.create_exp_tower(self.primitive_roots[0], i).fast_exponentiation(self.mod))
        else:
            primitive_base_root = Remainder_cyclic_group(self.base).primitive_roots
            self.primitive_roots.append(
                ModularCongruence.normalize((self.base + 1) * (primitive_base_root[0]), self.base))
            for i in range(2, self.euler_value):
                if EuclidAlgorithm.get_gcd(i, self.euler_value) == 1:
                    self.primitive_roots.append(
                        ExponentialTower.create_exp_tower(self.primitive_roots[0], i).fast_exponentiation(self.mod))
        self.primitive_roots.sort()
