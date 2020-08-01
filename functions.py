import math
import numpy as np
from abc import ABCMeta, abstractmethod

# np.random.seed(42)

class AFunction:
    __metaclass__ = ABCMeta

    upper_bound = 100
    lower_bound = -100

    @abstractmethod
    def calculate_fitness(self, position):
        pass


class Sphere(AFunction):

    def __init__(self):
        AFunction.upper_bound = 100
        AFunction.lower_bound = -100

    def calculate_fitness(self, position_list):
        solution = 0
        for position in position_list:
            solution += position ** 2
        return solution


class Rastrigin(AFunction):

    def __init__(self):
        AFunction.upper_bound = 5.12
        AFunction.lower_bound = -5.12

    def calculate_fitness(self, x):
        f_x = [xi ** 2 - 10 * math.cos(2 * math.pi * xi) + 10 for xi in x]
        return sum(f_x)


class Rosenbrocks(AFunction):

    def __init__(self):
        AFunction.upper_bound = 30
        AFunction.lower_bound = -30

    def calculate_fitness(self, x):
        sum_ = 0.0
        for i in range(1, len(x) - 1):
            sum_ += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
        return sum_
