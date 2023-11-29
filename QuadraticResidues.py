import Factorization
import PrimalityTest


class LegendreSymbol:
    def __init__(self, upper_value, lower_value):
        if lower_value != 2:
            self.upper = upper_value
            self.lower = lower_value
        else:
            raise Exception("Error! Lower value has to be an odd prime!")
        # self.print()

    def calculate(self):
        # non-prime case

        # base cases
        if self.upper == -1:
            if self.lower % 4 == 1:
                return 1
            elif self.lower % 4 == 3:
                return -1
        elif self.upper == 2:
            if self.lower % 8 == 1 or self.lower % 8 == 7:
                return 1
            elif self.lower % 8 == 3 or self.lower % 8 == 5:
                return -1
        elif self.upper == 1:
            return 1
        elif Factorization.is_perfect_square(self.upper):
            return 1
        # recursive cases
        else:
            factorization = Factorization.Factorize(self.upper)
            exponents = PrimalityTest.get_exponent_primes(self.upper)
            if len(factorization) > 1:
                temp_value = 1
                for i in range(len(factorization)):
                    temp_value *= LegendreSymbol(factorization[i] ** exponents[i], self.lower).calculate()
                return temp_value
            elif self.upper % self.lower != self.upper:
                return LegendreSymbol(self.upper % self.lower, self.lower).calculate()
            else:
                if self.upper % 4 == 1 or self.lower % 4 == 1:
                    return LegendreSymbol(self.lower, self.upper).calculate()
                elif self.upper % 4 == 3 and self.lower % 4 == 3:
                    return -LegendreSymbol(self.lower, self.upper).calculate()

    def print(self):
        print("({}/{})".format(self.upper, self.lower))





