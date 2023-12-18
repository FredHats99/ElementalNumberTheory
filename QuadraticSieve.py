import math

import IndexComputeAlgorithm
import QuadraticResidues


def get_candidate_set_from(n):
    set_values = []
    radius = int(math.e ** math.sqrt(math.log(n, math.e) * (math.log(math.log(n, math.e), math.e))))
    center = int(math.sqrt(n))
    print("M = {}".format(radius))
    for i in range(center - int(radius/2), center + int(radius/2)):
        set_values.append(i)
    print("I = {}".format(set_values))
    return set_values


def filter_base_factor(n, sm_bound):
    # n: the composite number
    # sm_bound: the smoothness bound
    # return: filtered smoothness bound
    filtered_sm = []
    base_factor = sm_bound.absolute_base_factor
    for i in base_factor:
        if i == -1 or i == 2:
            filtered_sm.append(i)
        else:
            if QuadraticResidues.LegendreSymbol(n, i).calculate() == 1:
                filtered_sm.append(i)
    return filtered_sm


def get_sieves(n, m):
    # n: the integer to factorize
    # m: the smoothness bound that will be used
    # return: a_j values to use for Legèndre Factorization
    sieves = []
    candidate_set = get_candidate_set_from(n)
    smooth_number = IndexComputeAlgorithm.Smooth_number(m)
    filtered_base_factor = filter_base_factor(n, smooth_number)
    num_of_values = len(filtered_base_factor) - 1
    # initializing complex vector
    vector = []
    for i in candidate_set:
        # Already applied treatment for p == -1
        vector.append([i, int(math.fabs((i ** 2) - n))])
    print("Vector = {}".format(vector))
    print("F''({}) = {}".format(m, filtered_base_factor))
    for j in filtered_base_factor:
        if j == -1:
            pass
        else:
            print("case p = {}".format(j))
            exponent = 1
            counter = -1
            while counter != 0:
                print("Subcase p = {}, exponent = {}".format(j, exponent))
                counter = 0
                a_0 = QuadraticResidues.sqrt(n, j ** exponent)
                print("a_0 = {}".format(a_0))
                if type(a_0) != list:
                    for k in range(len(vector)):
                        if vector[k][0] % (j ** exponent) == a_0:
                            counter += 1
                            vector[k][1] = int(vector[k][1]/j)
                    print("Vector = {}".format(vector))
                else:
                    for z in a_0:
                        for k in range(len(vector)):
                            if vector[k][0] % (j ** exponent) == z:
                                counter += 1
                                vector[k][1] = int(vector[k][1] / j)
                        print("Vector = {}".format(vector))
                exponent += 1
    for i in vector:
        if i[1] == 1:
            sieves.append(i[0])
    return sieves





