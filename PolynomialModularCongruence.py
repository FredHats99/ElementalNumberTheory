import math

import ModularCongruence


class create_polynome:
    def __init__(self, coefficients, variable):
        self.degree = len(coefficients) -1
        self.variable = variable
        self.coefficients = coefficients

    def show(self):
        string = ""
        for i in range(self.degree +1):
            if i != self.degree and i != self.degree - 1:
                if self.coefficients[i] != 1 and self.coefficients[i] > 0:
                    string += "+{}{}^{}".format(self.coefficients[i], self.variable, self.degree - i)
                elif self.coefficients[i] == 1:
                    string += "+{}^{}".format(self.variable, self.degree - i)
                elif self.coefficients[i] < 0:
                    string += "{}{}^{}".format(self.coefficients[i], self.variable, self.degree - i)
            elif i == self.degree - 1:
                if self.coefficients[i] != 1 and self.coefficients[i] > 0:
                    string += "+{}{}".format(self.coefficients[i], self.variable)
                elif self.coefficients[i] == 1:
                    string += "+{}^{}".format(self.variable, self.degree - i)
                elif self.coefficients[i] < 0:
                    string += "{}{}".format(self.coefficients[i], self.variable)
            elif i == self.degree:
                if self.coefficients[i] != 1 and self.coefficients[i] > 0:
                    string += "+{}".format(self.coefficients[i])
                elif self.coefficients[i] == 1:
                    string += "+{}".format(self.coefficients[i])
                elif self.coefficients[i] < 0:
                    string += "{}".format(self.coefficients[i])
        print(string)

    def modulate(self, mod):
        new_coefficients = []
        for i in range(self.degree+1):
            temp_coefficient = ModularCongruence.normalize(self.coefficients[i], mod)
            new_coefficients.append(temp_coefficient)
        return create_polynome(new_coefficients, self.variable)

    def equals(self, other, modulo):
        if self.degree < other.degree:
            zeros = []
            for i in range(other.degree - self.degree):
                zeros.append(0)
            zeros.extend(self.coefficients)
            self.coefficients = zeros
            self.degree += other.degree - self.degree
        elif self.degree > other.degree:
            zeros = []
            for i in range(self.degree - other.degree):
                zeros.append(0)
            zeros.extend(other.coefficients)
            other.coefficients = zeros
            other.degree += self.degree - other.degree
        normalized_other = other.modulate(modulo)
        for j in range(self.degree):
            if ModularCongruence.normalize(self.coefficients[j], modulo) != normalized_other.coefficients[j]:
                return False
        return True


def generate_from_Newton(values, number):
    coefficients = []
    for i in range(number+1):
        coefficients.append(math.comb(number, i) * values[0]**(number-i) * values[1]**i)
    return create_polynome(coefficients, "x")
