import DiofantineEquation
import GroupsTheory
import ModularCongruence


class DiscreteLog:
    def __init__(self, prime, primroot, value):
        self.prime = prime
        self.primeroot = primroot
        self.value = value

    def solve_first_mode(self):
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

    def solve_second_mode(self):
        eq = DiofantineEquation.create_equation(["x", "y"], [self.primeroot - 1, -self.prime], self.value - 1)
        partial_solution = ModularCongruence.normalize(ModularCongruence.parse_fixed_value(eq.solve()[0]), self.prime)
        print("Partial solution is: {}".format(partial_solution))
        counter = 0
        inverse_congr = ModularCongruence.init_congruence(self.primeroot, "x", 1, self.prime).solve()
        inverse = ModularCongruence.parse_fixed_value(inverse_congr)
        print("Inverse of {} modulo {} is {}".format(self.primeroot, self.prime, inverse))
        while partial_solution != 0:
            print("Iteration with counter = {}...".format(counter))
            partial_solution = ModularCongruence.normalize((partial_solution - 1) * inverse, self.prime)
            print("Calculation for this iteration yielded value: {}".format(partial_solution))
            counter += 1
        return counter
