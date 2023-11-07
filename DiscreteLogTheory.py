import DiofantineEquation
import ExponentialTower
import GroupsTheory
import ModularCongruence
import PrimalityTest


class DiscreteLog:
    def __init__(self, prime, primroot, value):
        self.prime = prime
        self.primeroot = primroot
        self.value = value

    def cappellini(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primeroot - 1, -self.prime], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.prime)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0
        while partial_solution != 0:
            print("Iteration with counter = {}...".format(counter))
            partial_solution = ModularCongruence.normalize(
                partial_solution - ModularCongruence.normalize(self.primeroot ** counter, self.prime), self.prime)
            print("Calculation for this iteration yielded value: {}".format(partial_solution))
            counter += 1
        return counter

    def cappellini_v2(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primeroot - 1, -self.prime], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.prime)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0
        inverse_congr = ModularCongruence.init_congruence(self.primeroot, "x", 1, self.prime).solve()
        inverse = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(inverse_congr), self.prime)
        print("Inverse of {} (modulo {}) is {}".format(self.primeroot, self.prime, inverse))
        while partial_solution != 0:
            # print("Iteration with counter = {}...".format(counter))
            partial_solution = ModularCongruence.normalize((partial_solution - 1) * inverse, self.prime)
            # print("Calculation for this iteration yielded value: {}".format(partial_solution))
            counter += 1
        return counter

    def cappellini_v3(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primeroot - 1, -self.prime], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.prime)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0

    def hellman_pohlig_algorithm(self):
        return_values = []
        # primroot --> r
        # prime --> p
        # value --> a
        factorization = PrimalityTest.get_prime_factors(self.prime - 1, 2)
        for i in range(len(factorization)):
            b_vector = []
            factor = factorization[i][0]
            order = factorization[i][1]
            # Step 1: calculate r^((p-1)/q) (mod p)
            base_r = ExponentialTower.create_exp_tower(self.primeroot,
                                                       int((self.prime - 1) / factor)).fast_exponentiation(self.prime)
            j = 0
            a_j = self.value
            # print("a0 = {}".format(self.value))
            while j <= order - 1:
                # Step 4: calculate a_j^((p-1)/q^(j+1)) (mod p)
                base_a = ExponentialTower.create_exp_tower(a_j, int((self.prime - 1) / factor ** (j + 1))).fast_exponentiation(self.prime)
                # Step 5: Solve a simpler Discrete Log Problem using any algorithm. Solution is a coefficient b_j
                # print("Solving Discrete Log for base_r = {}, base_a = {}".format(base_r, base_a))
                b_j = DiscreteLog(self.prime, base_r, base_a).cappellini_v2()
                # print("b[{}] = {}".format(j, b_j))
                b_vector.append(b_j)
                # Step 7: Recursive step for a_j reinitialization
                a_j = ModularCongruence.normalize(a_j*ExponentialTower.create_exp_tower(self.primeroot, (-b_j*(factor**j))).compute(self.prime), self.prime)
                # print("a[{}] = {}".format(j+1, a_j))
                j += 1
            k_value = 0
            for i in range(len(b_vector)):
                k_value += b_vector[i]*(factor**i)
            return_values.append([1, k_value, factor**order])
        return return_values

    def solve_with_hellman_pohlig(self):
        congr_system = self.hellman_pohlig_algorithm()
        system = ModularCongruence.init_system_of_congruences(congr_system)
        return system.general_solve()



