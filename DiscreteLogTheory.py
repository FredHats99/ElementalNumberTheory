import DiofantineEquation
import ExponentialTower
import Factorization
import GroupsTheory
import ModularCongruence
import PrimalityTest


class DiscreteLog:
    def __init__(self, modulo, primitive_root, value):
        self.mod = modulo
        # self.cyclic_group = GroupsTheory.Remainder_cyclic_group(self.mod)
        self.primitive_root = primitive_root
        self.value = value

    def cappellini(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primitive_root - 1, -self.mod], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.mod)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0
        while partial_solution != 0:
            print("Iteration with counter = {}...".format(counter))
            partial_solution = ModularCongruence.normalize(
                partial_solution - ModularCongruence.normalize(self.primitive_root ** counter, self.mod), self.mod)
            print("Calculation for this iteration yielded value: {}".format(partial_solution))
            counter += 1
        return counter

    def cappellini_v2(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primitive_root - 1, -self.mod], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.mod)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0
        inverse_congr = ModularCongruence.init_congruence(self.primitive_root, "x", 1, self.mod).solve()
        inverse = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(inverse_congr), self.mod)
        print("Inverse of {} (modulo {}) is {}".format(self.primitive_root, self.mod, inverse))
        while partial_solution != 0:
            # print("Iteration with counter = {}...".format(counter))
            partial_solution = ModularCongruence.normalize((partial_solution - 1) * inverse, self.mod)
            # print("Calculation for this iteration yielded value: {}".format(partial_solution))
            counter += 1
        print("log(base {}) of {} == {} (mod {})".format(self.primitive_root, self.value, counter, self.mod))
        return counter

    def cappellini_v3(self):
        partial_value = ModularCongruence.normalize(
            (self.value - 1) * GroupsTheory.Remainder_class(self.primitive_root - 1, self.mod).get_reciprocal().value,
            self.mod)
        mul_coefficient = GroupsTheory.Remainder_class(self.primitive_root, self.mod).get_reciprocal().value
        counter = 0
        while partial_value != 0:
            partial_value = ModularCongruence.normalize((partial_value - 1) * mul_coefficient, self.mod)
            counter += 1
        print("Log(base {}){} = {} (mod {})".format(self.primitive_root, self.value, counter, self.mod))

    def hellman_pohlig_algorithm(self):
        return_values = []
        # primroot --> r
        # prime --> p
        # value --> a
        factorization = Factorization.Factorize(self.mod - 1)
        for i in range(len(factorization)):
            b_vector = []
            factor = factorization[i][0]
            order = factorization[i][1]
            # Step 1: calculate r^((p-1)/q) (mod p)
            base_r = ExponentialTower.create_exp_tower(self.primitive_root,
                                                       int((self.mod - 1) / factor)).fast_exponentiation(self.mod)
            j = 0
            a_j = self.value
            # print("a0 = {}".format(self.value))
            while j <= order - 1:
                # Step 4: calculate a_j^((p-1)/q^(j+1)) (mod p)
                base_a = ExponentialTower.create_exp_tower(a_j,
                                                           int((self.mod - 1) / factor ** (j + 1))).fast_exponentiation(
                    self.mod)
                # Step 5: Solve a simpler Discrete Log Problem using any algorithm. Solution is a coefficient b_j
                # print("Solving Discrete Log for base_r = {}, base_a = {}".format(base_r, base_a))
                b_j = DiscreteLog(self.mod, base_r, base_a).cappellini_v2()
                # print("b[{}] = {}".format(j, b_j))
                b_vector.append(b_j)
                # Step 7: Recursive step for a_j reinitialization
                a_j = ModularCongruence.normalize(
                    a_j * ExponentialTower.create_exp_tower(self.primitive_root, (-b_j * (factor ** j))).compute(
                        self.mod), self.mod)
                # print("a[{}] = {}".format(j+1, a_j))
                j += 1
            k_value = 0
            for i in range(len(b_vector)):
                k_value += b_vector[i] * (factor ** i)
            return_values.append([1, k_value, factor ** order])
        return return_values

    def solve_with_hellman_pohlig(self):
        congr_system = self.hellman_pohlig_algorithm()
        system = ModularCongruence.init_system_of_congruences(congr_system)
        return system.general_solve()
