import DiofantineEquation


class init_congruence:
    def __init__(self, coefficient, variable, value, modulo):
        self.coefficient = coefficient
        self.variable = variable
        self.value = value
        self.mod = modulo
        self.equation = self.print()
        self.solution = ""

    def solve(self):
        temp_variable = [self.variable, "y"]
        temp_coefficient = [self.coefficient, self.mod]
        temp_equation = DiofantineEquation.create_equation(temp_variable, temp_coefficient, self.value)
        self.solution = temp_equation.solve()[0]
        print("[ModularCongruence.py]: Request {} solved with solution {}".format(self.equation, self.solution))
        return self.solution

    def print(self):
        return "{}{} = {} (mod {})".format(self.coefficient, self.variable, self.value, self.mod)


class init_system_of_congruences:
    def __init__(self, matrix):
        self.num_of_congruences = len(matrix)
        self.congruences = []
        self.matrix = matrix
        assert len(matrix[0]) == 3
        self.simplify()
        self.system = self.print()

    def simplify(self):
        for i in range(self.num_of_congruences):
            coefficient = self.matrix[i][0]
            value = self.matrix[i][1]
            modulo = self.matrix[i][2]
            coefficient = coefficient % modulo
            value = value % modulo
            i_congruence = init_congruence(coefficient, "x_{}".format(i), value, modulo)
            i_congruence.solve()
            self.matrix[i][0] = 1
            self.matrix[i][1] = int(i_congruence.solution.split(" ")[0])
            self.matrix[i][2] = abs(int(i_congruence.solution.split(" ")[2].split("k")[0]))
            self.congruences.append(i_congruence)
            self.normalize(i)

    def solve_for_two(self, index_1, index_2):
        coefficient = self.matrix[index_1][2]
        value = self.matrix[index_2][1] - self.matrix[index_1][1]
        new_congruence = init_congruence(coefficient, "x", value, self.matrix[index_2][2])
        new_congruence.solve()
        string = "{} + {}{}".format(
            normalize(self.matrix[index_1][1] + self.matrix[index_1][2] * int(new_congruence.solution.split(" ")[0]),
                      self.matrix[index_1][2] * self.matrix[index_2][2]),
            self.matrix[index_1][2] * self.matrix[index_2][2], "l")
        return string

    def general_solve(self):
        for i in range(self.num_of_congruences - 1):
            partial_solution = self.solve_for_two(i, i + 1)
            if i == self.num_of_congruences - 2:
                self.normalize(i + 1)
                print("[ModularCongruence.py]: Request:\n{}solved with solution {}".format(self.system, partial_solution))
                return parse_fixed_value(partial_solution)
            self.matrix[i + 1][1] = int(partial_solution.split(" ")[0])
            self.matrix[i + 1][2] = int(partial_solution.split(" ")[2].split("l")[0])
            self.normalize(i + 1)

    def normalize(self, i):
        while self.matrix[i][1] < 0:
            self.matrix[i][1] += self.matrix[i][2]
        while self.matrix[i][1] > self.matrix[i][2]:
            self.matrix[i][1] -= self.matrix[i][2]

    def print(self):
        string = ""
        for i in range(len(self.congruences)):
            string += "|{}\n".format(self.congruences[i].equation)
        return string


def normalize(a, b):
    try:
        a = a % b
    except ZeroDivisionError:
        a = 0
    return a


def parse_fixed_value(string):
    return int(string.split(" ")[0])


def parse_coefficient(string, variable):
    return int(string.split(" ")[2].split(variable)[0])
