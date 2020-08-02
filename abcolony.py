import random
import numpy as np
from numpy.random import choice

from particle import BeeJob, Bee
from functions import Rastrigin


class ABC:

    def __init__(
            self, fail_limit=200, population_size=30, dimensions=30, max_iterations=10000,
            objective_function=Rastrigin()):
        self.population_size = population_size
        self.dimensions = dimensions
        self.max_iterations = max_iterations
        self.objective_function = objective_function
        self.fail_limit = fail_limit

        self.colony = []
        self.best_fitness = float('inf')
        self.list_best_fitness = []

    def _get_random_positions(self):
        return [
            self.objective_function.lower_bound + random.uniform(0, 1) * (self.objective_function.upper_bound - self.objective_function.lower_bound)
            for _ in range(self.dimensions)
        ]

    def initialize_colony(self):
        self.colony = [
            Bee(
                objective_function=self.objective_function,
                positions=self._get_random_positions(),
                bee_type=BeeJob.EMPLOYED,
            )
            for _ in range(self.population_size//2)
        ]
        self.colony += [
            Bee(
                objective_function=self.objective_function,
                positions=[],
                bee_type=BeeJob.ONLOOKERS,
            )
            for _ in range(self.population_size//2)
        ]

    def evaluate_colony(self):
        for bee in self.colony:
            bee.evaluate()

    def update_best_solution(self):
        current_min = min([bee.fitness for bee in self.colony if bee.bee_type == BeeJob.EMPLOYED])
        if self.best_fitness > current_min:
            self.best_fitness = current_min

    def employed_bees_exploration(self):
        for i in range(len(self.colony)//2):
            bee = self.colony[i]
            bee.employed_bees_explore_new_food_source()

    def calculate_probabilities_for_onlookers(self):
        employer_bees_fitness_sum = sum(
            [self.colony[i].fitness for i in range(len(self.colony))]
        )
        probability_distribution = [
            (self.colony[i].fitness / employer_bees_fitness_sum)
            for i in range(len(self.colony)//2)
        ]
        # probability_distribution = [
        #     (0.9 * (bee.fitness / employer_bees_fitness_max)) + 0.1
        #     for bee in self.colony if bee.bee_type == BeeJob.EMPLOYED
        # ]
        probability_distribution = np.array(probability_distribution)
        probability_distribution /= probability_distribution.sum()
        return probability_distribution

    def onlooker_bees_exploration(self):
        probability_distribution = self.calculate_probabilities_for_onlookers()
        employed_bees = [bee for bee in self.colony if bee.bee_type == BeeJob.EMPLOYED]

        for t in range(len(self.colony)//2):
            lead_bee = choice(employed_bees, 1, p=probability_distribution)[0]

            bee = self.colony[t + 15]
            bee.set_new_food_source_for_onlooker_bee(list(lead_bee.current_position))

            if bee.fitness < lead_bee.fitness:
                lead_bee.current_position = list(bee.current_position)
                lead_bee.fitness = bee.fitness
                lead_bee.failures = 0
            else:
                lead_bee.failures += 1

    def scount_bees_exploration(self):
        for bee in self.colony:
            if bee.failures > self.fail_limit:
                bee.current_position = self._get_random_positions()

    def search(self):
        self.initialize_colony()
        self.evaluate_colony()
        self.update_best_solution()

        for i in range(self.max_iterations):
            self.employed_bees_exploration()
            self.calculate_probabilities_for_onlookers()

            self.onlooker_bees_exploration()
            self.scount_bees_exploration()
            self.evaluate_colony()
            self.update_best_solution()
            print(f"Best: {self.best_fitness}. Iteration: {i}")
            self.list_best_fitness.append(self.best_fitness)
        return self.list_best_fitness

