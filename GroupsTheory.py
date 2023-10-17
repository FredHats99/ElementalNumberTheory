import ExponentialTower
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
            return None


class Remainder_set_group:
    def __init__(self, modulo):
        self.mod = modulo
        self.remainder_classes = []
        self.reciprocal_subset = []
        for i in range(self.mod):
            rem_class = Remainder_class(i, self.mod)
            self.remainder_classes.append(rem_class)

    def get_reciprocal_subset(self):
        for i in range(1, self.mod):
            value = self.remainder_classes[i].get_reciprocal()
            if value is not None:
                self.reciprocal_subset.append(self.remainder_classes[i].value)

    def get_Euler_value(self):
        self.get_reciprocal_subset()
        return len(self.reciprocal_subset)


def get_prime_divisors_of(subset, param):
    prime_divisors = []
    for i in range(len(subset)):
        if EuclidAlgorithm.get_gcd(subset[i], param) != 1 and PrimalityTest.AKS_simple_criteria(subset[i]):
            prime_divisors.append(subset[i])
    return prime_divisors


class Remainder_set_cyclic_group(Remainder_set_group):
    def __init__(self, modulo):
        assert PrimalityTest.AKS_simple_criteria(modulo)
        super().__init__(modulo)

    def get_primitive_roots(self):
        primitive_roots = []
        self.get_reciprocal_subset()
        prime_divisors = get_prime_divisors_of(self.reciprocal_subset, self.get_Euler_value())
        for i in range(1, len(self.remainder_classes)):
            for j in range(len(prime_divisors)):
                if ExponentialTower.create_exp_tower(self.remainder_classes[i].value, int(self.mod/prime_divisors[j])).fast_exponentiation(self.mod) == 1:
                    break
                if j == len(prime_divisors)-1:
                    primitive_roots.append(self.remainder_classes[i].value)
        return primitive_roots







