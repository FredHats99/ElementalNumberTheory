import math

import EuclidAlgorithm
import Teacher


class create_equation:
    def __init__(self, variables, coeffs, value):
        assert 1 < len(coeffs) == len(variables)
        self.variables = variables
        self.coefficients = coeffs
        self.value = value
        self.gcd = 0
        self.equation = self.write()

    def is_there_a_solution(self, print_steps):
        self.gcd = EuclidAlgorithm.get_multiple_gcd(self.coefficients, print_steps=print_steps)
        if self.value % self.gcd == 0:
            return True
        return False

    def write(self):
        string = ""
        for i in range(len(self.variables)):
            if self.coefficients[i] > 0:
                string += "+{}{} ".format(self.coefficients[i], self.variables[i])
            else:
                string += "{}{} ".format(self.coefficients[i], self.variables[i])
        string += "= {}".format(self.value)
        return string

    @Teacher.teach
    def solve(self, print_steps):
        if self.is_there_a_solution(print_steps=print_steps):
            if len(self.coefficients) == 2:
                x, y, gcd = EuclidAlgorithm.get_extended_gcd(self.coefficients[0], self.coefficients[1], print_steps, print_steps=print_steps)
                solution = "{} + {}k".format((int(x * self.value / gcd)) % int(math.fabs(self.coefficients[1])),
                                             self.coefficients[1]), "{} - {}k".format(
                    int((y * self.value / gcd)) % self.coefficients[0], self.coefficients[0])
                yield "[DiophantineEquation.solve({})]: equation solved with solutions {}".format(self.equation,
                                                                                                     solution)
                return solution
            else:
                temp_eq = create_equation(self.variables[0: 2], self.coefficients[0: 2], self.value)
                a, b = temp_eq.solve()
                solution = []
                for i in range(2, len(self.coefficients)):
                    a = a + " + {}{}".format(self.coefficients[i], self.variables[i])
                    b = b + " - {}{}".format(self.coefficients[i], self.variables[i])
                solution.append(a)
                solution.append(b)
                for i in range(2, len(self.coefficients)):
                    solution.append("{}{}".format(self.gcd, self.variables[i]))
                print(
                    "[DiophantineEquation.py]: equation '{}' solved with solutions {}".format(self.equation, solution))
                return solution
