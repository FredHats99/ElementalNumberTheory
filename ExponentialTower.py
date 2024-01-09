import ModularCongruence
import GroupsTheory
import Teacher


def get_base2(exponent):
    base2_list = []
    tmp_exp = exponent
    while tmp_exp != 0:
        base2_list.append(int(tmp_exp % 2))
        if tmp_exp % 2 == 0:
            tmp_exp = tmp_exp/2
        else:
            tmp_exp = (tmp_exp-1)/2
    return base2_list


class create_exp_tower:
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
        self.value = 0
        self.tower = self.show()

    def show(self):
        if not isinstance(self.exponent, create_exp_tower):
            string = "{}^{}".format(self.base, self.exponent)
        else:
            string = "{}^".format(self.base) + "({})".format(self.exponent.show())
        return string

    def calculate(self):
        return self.base ** self.exponent

    def compute(self, value):
        newBase = ModularCongruence.normalize(self.base, value)
        if not isinstance(self.exponent, create_exp_tower):
            newExp = ModularCongruence.normalize(self.exponent, GroupsTheory.Remainder_group(value).euler_value)
            # print("New base is: {}, new exponent is {}, computation is {}".format(newBase, newExp, newBase ** newExp))
            return newBase ** newExp
        else:
            newExp = self.exponent.fast_exponentiation(GroupsTheory.Remainder_group(value).euler_value)
            newTower = create_exp_tower(self.base, newExp)
            print("[ExponentialTower.py]: reducing to {} modulo {}".format(newTower.tower, value))
            return newTower.fast_exponentiation(value)

    def bruteforce_remainder(self, value):
        self.base = ModularCongruence.normalize(self.base, value)
        # print("The base has been reduced to {}".format(self.base))
        eq = ModularCongruence.init_congruence(1, "x", self.compute(value), value)
        # eq.print()
        eq.solve()
        return ModularCongruence.normalize(int(ModularCongruence.parse_fixed_value(eq.solution)), value)

    @Teacher.teach
    def fast_exponentiation(self, mod):
        yield"[ExponentialTower.fast_exponentiation({})]: Requesting fast-exponentiation modulo {}".format(self.tower, mod)
        if not isinstance(self.exponent, int):
            return self.compute(mod)
        base2_exp = get_base2(self.exponent)
        base2_remainders = []

        for i in range(len(base2_exp)):
            if i == 0:
                base2_remainders.append(self.base)
            else:
                base2_remainders.append(ModularCongruence.normalize(base2_remainders[i-1]**2, mod))
        # print(base2_exp)
        # print(base2_remainders)
        temp_value = 1
        for j in range(len(base2_remainders)):
            if base2_exp[j] == 1:
                temp_value *= base2_remainders[j]
        yield"[ExponentialTower.py]: fast-exponentiated {} to {} modulo {}".format(self.tower, ModularCongruence.normalize(temp_value, mod), mod)
        return ModularCongruence.normalize(temp_value, mod)




