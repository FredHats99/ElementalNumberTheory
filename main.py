import EuclidAlgorithm
import DiofantineEquation
import ExponentialTower
import ModularCongruence
import GroupsTheory


def main():
    # Test section
    example = ExponentialTower.create_exp_tower(6, 73)
    print(example.fast_exponentiation(100))


main()
