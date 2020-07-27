import copy
import numpy as np
import functools
import random
import math

from particle import Fish
from parameters import num_of_individuos, dimensions, iterations_number

np.random.seed(42)

class FSS():

    def __init__(self, objective_function):
        self.function = objective_function
        self.dimensions = dimensions
        self.iterations_number = iterations_number
        self.num_of_individuos = num_of_individuos
        self.cluster = []
        self.global_best = float('inf')
        self.global_best_position = []

        # Params
        self.total_weight = 1 * self.num_of_individuos
        self.initial_step_ind = 0.1
        self.final_step_ind = 0.0001
        self.step_ind = self.initial_step_ind * (objective_function.upper_bound - objective_function.lower_bound)
        self.initial_step_vol = 0.01
        self.final_step_vol = 0.001
        self.step_vol = self.initial_step_vol * (objective_function.upper_bound - objective_function.lower_bound)
        self.list_global_best_values = []

    def search(self):
        self._initialize_cluster()

        for i in range(self.iterations_number):
            self.evaluate_cluster()
            self.updates_optimal_solution()

            self.apply_individual_movement()
            self.evaluate_cluster()
            self.updates_optimal_solution()

            self.apply_feeding()

            self.apply_instintive_collective_movement()
            self.apply_collective_volitive_movement()

            self.update_step(i)
            self.update_total_weight()

            self.evaluate_cluster()
            self.updates_optimal_solution()
            self.list_global_best_values.append(self.global_best)
            print("iter: {} = cost: {}".format(i, self.global_best))

    def update_total_weight(self):
        self.total_weight = sum([fish.weight for fish in self.cluster])

    def _initialize_cluster(self):
        self.cluster = []
        for _ in range(self.num_of_individuos):
            fish = Fish(
                positions=[self._get_random_number() for _ in range(dimensions)],
                objective_function=self.function
            )
            self.cluster.append(fish)

    def evaluate_cluster(self):
        for fish in self.cluster:
            fish.evaluate()

    def updates_optimal_solution(self):
        for fish in self.cluster:
            if fish.fitness < self.global_best:
                self.global_best = fish.fitness
                self.global_best_position = list(fish.current_position)

    def apply_individual_movement(self):
        for fish in self.cluster:
            fish.update_position_individual_movement(self.step_ind)

    def apply_feeding(self):
        max_delta_fitness = max([fish.delta_fitness for fish in self.cluster])
        for fish in self.cluster:
            fish.feed(max_delta_fitness)

    def apply_instintive_collective_movement(self):
        sum_delta_fitness = sum([fish.delta_fitness for fish in self.cluster])

        for fish in self.cluster:
            fish.update_position_collective_movement(sum_delta_fitness)

    def _calculate_barycenter(self):
        sum_weights = sum([fish.weight for fish in self.cluster])
        sum_position_and_weights = [[x * fish.weight for x in fish.current_position] for fish in self.cluster]
        sum_position_and_weights = np.sum(sum_position_and_weights, 0)
        return [s / sum_weights for s in sum_position_and_weights]

    def apply_collective_volitive_movement(self):
        barycenter = self._calculate_barycenter()
        current_total_weight = sum([fish.weight for fish in self.cluster])
        search_operator = -1 if current_total_weight > self.total_weight else 1
        for fish in self.cluster:
            fish.update_position_volitive_movement(barycenter, self.step_vol, search_operator)

    def update_step(self, current_i):
        self.step_ind = self.initial_step_ind - current_i * float(
            self.initial_step_ind - self.final_step_ind) / iterations_number
        self.step_vol = self.initial_step_vol - current_i * float(
            self.initial_step_vol - self.final_step_vol) / iterations_number

    def _get_random_number(self):
        return np.random.uniform(self.function.lower_bound, self.function.upper_bound)
