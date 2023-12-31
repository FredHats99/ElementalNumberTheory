import DiscreteLogTheory
import ExponentialTower
import Factorization
import GroupsTheory
import PrimalityTest


class LegendreSymbol:
    def __init__(self, upper_value, lower_value):
        self.upper = upper_value
        self.lower = lower_value
        # self.print()

    def calculate(self):
        # trivial case
        if self.lower % self.upper == 0:
            return 0
        # remove square cases
        fact_exponents = PrimalityTest.get_exponent_primes(self.upper)
        prime_factors = Factorization.Factorize(self.upper)
        for i in range(len(fact_exponents)):
            if fact_exponents[i] >= 2:
                print("Legendre({},{}) --> Legendre({},{})".format(self.upper, self.lower,
                                                                   int(self.upper / ((prime_factors[i]) ** 2)),
                                                                   self.lower))
                return LegendreSymbol(int(self.upper / ((prime_factors[i]) ** 2)), self.lower).calculate()
        # non-prime case
        if not PrimalityTest.is_prime(self.upper) and PrimalityTest.is_prime(self.lower):
            print("Legendre({},{}) ---> Jacobi({},{})".format(self.upper, self.lower, self.upper, self.lower))
            return JacobiSymbol(self.upper, self.lower).calculate()
        # base cases
        if self.upper == -1:
            if self.lower % 4 == 1:
                print("Legendre({},{}) --> 1".format(self.upper, self.lower))
                return 1
            elif self.lower % 4 == 3:
                print("Legendre({},{}) --> -1".format(self.upper, self.lower))
                return -1
        elif self.upper == 2:
            if self.lower % 8 == 1 or self.lower % 8 == 7:
                print("Legendre({},{}) --> 1".format(self.upper, self.lower))
                return 1
            elif self.lower % 8 == 3 or self.lower % 8 == 5:
                print("Legendre({},{}) --> -1".format(self.upper, self.lower))
                return -1
        elif self.upper == 1:
            print("Legendre({},{}) --> 1".format(self.upper, self.lower))
            return 1
        elif Factorization.is_perfect_square(self.upper):
            print("Legendre({},{}) --> 1".format(self.upper, self.lower))
            return 1
        # recursive cases
        else:
            if self.upper % 2 == 0:
                print(
                    "Legendre({},{}) = Legendre({},{}) * Legendre({},{})".format(self.upper, self.lower, 2, self.lower,
                                                                                 int(self.upper / 2), self.lower))
                return LegendreSymbol(2, self.lower).calculate() * LegendreSymbol(int(self.upper / 2),
                                                                                  self.lower).calculate()
            if self.upper % self.lower != self.upper:
                print("Legendre({},{}) --> Legendre({},{})".format(self.upper, self.lower, self.upper % self.lower,
                                                                   self.lower))
                return LegendreSymbol(self.upper % self.lower, self.lower).calculate()
            else:
                if self.upper % 4 == 1 or self.lower % 4 == 1:
                    print("Legendre({},{}) --> Legendre({},{})".format(self.upper, self.lower, self.lower, self.upper))
                    return LegendreSymbol(self.lower, self.upper).calculate()
                elif self.upper % 4 == 3 and self.lower % 4 == 3:
                    print(
                        "Legendre({},{}) --> - Legendre({},{})".format(self.upper, self.lower, self.lower, self.upper))
                    return -1 * LegendreSymbol(self.lower, self.upper).calculate()

    def print(self):
        print("({}/{})".format(self.upper, self.lower))


class JacobiSymbol:
    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower

    def calculate(self):
        # remove square cases
        fact_exponents = PrimalityTest.get_exponent_primes(self.upper)
        prime_factors = Factorization.Factorize(self.upper)
        for i in range(len(fact_exponents)):
            if fact_exponents[i] >= 2:
                print("Jacobi({},{}) --> Jacobi({},{})".format(self.upper, self.lower,
                                                               int(self.upper / ((prime_factors[i]) ** 2)),
                                                               self.lower))
                return JacobiSymbol(int(self.upper / ((prime_factors[i]) ** 2)), self.lower).calculate()
        # base cases
        if self.upper == -1:
            if self.lower % 4 == 1:
                print("Jacobi({},{}) --> 1".format(self.upper, self.lower))
                return 1
            elif self.lower % 4 == 3:
                print("Jacobi({},{}) --> -1".format(self.upper, self.lower))
                return -1
        elif self.upper == 2:
            if self.lower % 8 == 1 or self.lower % 8 == 7:
                print("Jacobi({},{}) --> 1".format(self.upper, self.lower))
                return 1
            elif self.lower % 8 == 3 or self.lower % 8 == 5:
                print("Jacobi({},{}) --> -1".format(self.upper, self.lower))
                return -1
        elif self.upper == 1:
            print("Jacobi({},{}) --> 1".format(self.upper, self.lower))
            return 1
        elif Factorization.is_perfect_square(self.upper):
            print("Jacobi({},{}) --> 1".format(self.upper, self.lower))
            return 1
        # recursive cases
        else:
            if self.upper % 2 == 0:
                print("Jacobi({},{}) = Jacobi({},{}) * Jacobi({},{})".format(self.upper, self.lower, 2, self.lower,
                                                                             int(self.upper / 2), self.lower))
                return JacobiSymbol(2, self.lower).calculate() * JacobiSymbol(int(self.upper / 2),
                                                                              self.lower).calculate()
            if self.upper % self.lower != self.upper:
                print("Jacobi({},{}) --> Jacobi({},{})".format(self.upper, self.lower, self.upper % self.lower,
                                                               self.lower))
                return JacobiSymbol(self.upper % self.lower, self.lower).calculate()
            else:
                if self.upper % 4 == 1 or self.lower % 4 == 1:
                    print("Jacobi({},{}) --> Jacobi({},{})".format(self.upper, self.lower, self.lower, self.upper))
                    return JacobiSymbol(self.lower, self.upper).calculate()
                elif self.upper % 4 == 3 and self.lower % 4 == 3:
                    print("Jacobi({},{}) --> - Jacobi({},{})".format(self.upper, self.lower, self.lower, self.upper))
                    return -JacobiSymbol(self.lower, self.upper).calculate()
                # by definition...
                lower_factorization = Factorization.Factorize(self.lower)
                lower_fact_exponents = PrimalityTest.get_exponent_primes(self.lower)
                value = 1
                for i in range(len(lower_factorization)):
                    print("Jacobi({},{}) --> (Legendre({},{}))^{}".format(self.upper, self.lower, self.upper,
                                                                          lower_factorization[i],
                                                                          lower_fact_exponents[i]))
                    value *= (LegendreSymbol(self.upper, lower_factorization[i]).calculate()) ** lower_fact_exponents[i]
                return value


def get_square_root(num, modulo):
    if PrimalityTest.is_prime(modulo):
        if LegendreSymbol(num, modulo).calculate() != 1:
            print("There is no square root for {} modulo {}".format(num, modulo))
        else:
            # exponent_2 --> s
            # odd_residue --> u
            # base --> b
            # non_quad_residue --> y
            # disc_log --> k
            # sub_group_generator --> z
            if modulo % 4 == 3:
                return ExponentialTower.create_exp_tower(num, int((modulo + 1) / 4)).fast_exponentiation(
                    modulo), modulo - ExponentialTower.create_exp_tower(num, int((modulo + 1) / 4)).fast_exponentiation(
                    modulo)
            elif modulo % 4 == 1:
                exponent_2 = PrimalityTest.get_exponent_primes(modulo - 1)[0]
                # print("s = {}".format(exponent_2))
                odd_residue = int((modulo - 1) / 2 ** exponent_2)
                # print("u = {}".format(odd_residue))
                base = ExponentialTower.create_exp_tower(num, odd_residue).fast_exponentiation(modulo)
                # print("b = {}".format(base))
                non_quad_residue = 1
                while LegendreSymbol(non_quad_residue, modulo).calculate() != -1:
                    non_quad_residue += 1
                # print("y = {}".format(non_quad_residue))
                sub_group_generator = ExponentialTower.create_exp_tower(non_quad_residue,
                                                                        2 * odd_residue).fast_exponentiation(modulo)
                # print("z = {}".format(sub_group_generator))
                # disc_log = DiscreteLogTheory.DiscreteLog(modulo, sub_group_generator % modulo, base).cappellini_v3()
                disc_log, z_star = get_K_not_with_log(exponent_2, base, modulo, non_quad_residue, odd_residue)
                # print("k = {}".format(disc_log))
                # solution = ((num ** int((odd_residue + 1) / 2)) * (GroupsTheory.Remainder_class(non_quad_residue, modulo).get_reciprocal().value ** (odd_residue * disc_log))) % modulo
                solution = (ExponentialTower.create_exp_tower(z_star, disc_log).fast_exponentiation(
                    modulo) * ExponentialTower.create_exp_tower(num, int((odd_residue + 1) / 2)).fast_exponentiation(
                    modulo)) % modulo
                return solution, -solution % modulo


def get_K_not_with_log(s, b, p, y, u):
    # p --> prime number
    # s --> exponent of highest power of 2 of p-1
    # b --> a^u (mod p)
    # y --> any n.r.q. modulo p
    # u --> odd remainder when extracting powers of 2 from p-1
    base2_J = []
    z_star = ExponentialTower.create_exp_tower(y, u).fast_exponentiation(p)
    for i in range(0, s - 1):
        # print("J in base 2: {}".format(base2_J))
        if i == 0:
            temp = ExponentialTower.create_exp_tower(b,
                                                     2 ** (s - 2)).fast_exponentiation(p)
            # print("temp = {}".format(temp))
            if temp == 1:
                base2_J.append(0)
            elif temp == p - 1:
                base2_J.append(1)
            else:
                raise Exception("Unexpected value --> {}".format(temp))
        else:
            temp_value = 0
            for j in range(len(base2_J)):
                # j --> k - 1
                temp_value += base2_J[j] * (2 ** j)
                # print("temp_value = {}".format(temp_value))
            temp_value = ExponentialTower.create_exp_tower(z_star, temp_value).fast_exponentiation(p)
            temp_value = ExponentialTower.create_exp_tower(temp_value, 2).fast_exponentiation(p)
            temp_value *= b
            temp_value = ExponentialTower.create_exp_tower(temp_value, 2 ** (s - 2 - i)).fast_exponentiation(
                p)
            if temp_value == 1:
                base2_J.append(0)
            elif temp_value == p - 1:
                base2_J.append(1)
            else:
                raise Exception("Unexpected value --> {}".format(temp_value))
    k = 0
    for i in range(len(base2_J)):
        k += base2_J[i] * (2 ** i)
    return k, z_star


def Shanks_Tonelli(num, mod):
    # a --> num
    # p --> mod
    assert PrimalityTest.is_prime(mod)
    assert LegendreSymbol(num, mod).calculate() == 1
    s = PrimalityTest.get_exponent_primes(mod - 1)[0]
    u = int((mod - 1) / 2 ** s)
    # p-1 = (2**s)*u
    y = 1
    while LegendreSymbol(y, mod).calculate() != -1:
        y += 1
    # y --> Any n.q.r. modulo p
    z_star = ExponentialTower.create_exp_tower(y, u).fast_exponentiation(mod)
    # z --> y**u (mod p)
    b = ExponentialTower.create_exp_tower(num, u).fast_exponentiation(mod)
    # b --> a**u (mod p)
    r = ExponentialTower.create_exp_tower(num, int((u + 1) / 2)).fast_exponentiation(mod)
    # r --> a**(u+1/2) (mod p)
    # print("{} - 1 = {}*(2**{}),\ny = {},\nz = {},\nb = {},\nr = {}".format(mod, u, s, y, z_star, b, r))
    while b != 1:
        # find k
        k, el = -1, -1
        value = 0
        while value != mod - 1:
            k += 1
            value = ExponentialTower.create_exp_tower(b, 2 ** k).fast_exponentiation(mod)
            # print("k = {}, value = {}".format(k, value))
        value = 0
        while value != mod - 1:
            el += 1
            value = ExponentialTower.create_exp_tower(z_star ** 2, el).fast_exponentiation(mod)
            # print("el = {}, value = {}".format(el, value))
        r *= ExponentialTower.create_exp_tower(z_star, 2 ** (el - k - 1)).fast_exponentiation(mod)
        b *= ExponentialTower.create_exp_tower(z_star, 2 ** (el - k)).fast_exponentiation(mod)
        z_star = ExponentialTower.create_exp_tower(z_star, 2 ** (el - k)).fast_exponentiation(mod)
        r = r % mod
        b = b % mod
        # print("r --> {}\nb --> {}\nz_star --> {}".format(r,b,z_star))
    # second solution: -r % mod
    return [r, -r % mod]


def sqrt(num, mod):
    factorization = PrimalityTest.is_composite(mod)
    if factorization is False and mod % 2 != 0:
        return Shanks_Tonelli(num, mod)
    elif mod % 2 != 0:
        prime = factorization[0][0]
        exponent = factorization[1][0]
        # ASSERTION: there is only one prime factor
        simple_root = Shanks_Tonelli(num, prime)[0]
        w = ExponentialTower.create_exp_tower(num, int(((prime ** exponent) - 2 * (prime ** (exponent-1)) + 1)/2)).fast_exponentiation(mod)
        v = ExponentialTower.create_exp_tower(simple_root, ExponentialTower.create_exp_tower(prime, exponent-1)).fast_exponentiation(mod)
        return [(w * v) % mod, - (w * v) % mod]
    else:
        try:
            exponent = factorization[1][0]
        except TypeError:
            exponent = 1
        if (exponent == 2 and num % 4 == 3) or (exponent >= 3 and num % 8 != 1):
            return "No Solution"
        elif exponent == 1:
            if num % 2 == 0:
                return 0
            else:
                return 1
        elif exponent == 2 and num % 4 == 1:
            return [1, -1]
        else:
            # Here 4 solutions are expected
            u = int((num-1)/8)
            root = -1
            for i in range(0,1):
                if (i**2 + i - 2*u) % 2 == 0:
                    root = i
            print("Base root = {}".format(root))
            k = 1
            while k <= exponent-2:
                root -= (root**2 + root - 2*u) * GroupsTheory.Remainder_class(2*root + 1, 2**k).get_reciprocal().value
                root = root % (2 ** k)
                print("k --> {}, newroot = {}".format(k, root))
                k += 1
            root = 2*root + 1
            return [root, -root % mod, root + 2 ** (exponent - 1), (-root + 2 ** (exponent - 1)) % mod]





