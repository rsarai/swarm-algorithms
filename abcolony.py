import random
import numpy as np
from numpy.random import choice

from particle import BeeJob, Bee
from functions import Rastrigin


class ABC:

    def __init__(
            self, update_type, fail_limit=200, population_size=30, dimensions=30, max_iterations=10000,
            objective_function=Rastrigin()):
        self.population_size = population_size
        self.dimensions = dimensions
        self.max_iterations = max_iterations
        self.objective_function = objective_function
        self.fail_limit = fail_limit
        self.update_type = update_type

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
                food_source=i,
            )
            for i in range(self.population_size//2)
        ]

        onlookers = []
        probability_distribution = self.calculate_probabilities_for_onlookers(self.colony)
        for _ in range(self.population_size//2):
            source = choice(self.colony, 1, p=probability_distribution)[0]
            food_source = self.colony.index(source)
            onlookers += [
                Bee(
                    objective_function=self.objective_function,
                    positions=source.current_position,
                    bee_type=BeeJob.ONLOOKERS,
                    food_source=food_source,
                )
            ]

        self.colony += onlookers

    def evaluate_colony(self):
        for bee in self.colony:
            bee.evaluate()

    def update_best_solution(self):
        current_min = min([bee.fitness for bee in self.colony if bee.bee_type == BeeJob.EMPLOYED])
        if self.best_fitness > current_min:
            self.best_fitness = current_min

    def employed_bees_exploration(self):
        for i in range(len(self.colony)//2 - 1, len(self.colony)):
            bee = self.colony[i]
            bee.employed_bees_explore_new_food_source()

    def calculate_probabilities_for_onlookers(self, bees):
        employer_bees_fitness_sum = sum([bee.fitness for bee in bees])
        if employer_bees_fitness_sum == 0:
            probability_distribution = [1/len(bees) for bee in bees]
        else:
            probability_distribution = [(bee.fitness / employer_bees_fitness_sum) for bee in bees]
        probability_distribution = np.array(probability_distribution)
        probability_distribution /= probability_distribution.sum()
        return probability_distribution

    def onlooker_bees_exploration(self):
        for t in range(len(self.colony)//2):
            bee = self.colony[t + 15]
            if self.update_type.value == 1:
                random_bee_index = random.randint(0, (self.dimensions/2) - 1)
                lead_bee = self.colony[random_bee_index]
            elif self.update_type.value == 2:
                bees_on_same_source = [b for b in self.colony if b.food_source == bee.food_source]
                lead_bee_index = random.randint(0, len(bees_on_same_source) - 1)
                lead_bee = bees_on_same_source[lead_bee_index]
                random_bee_index = bee.food_source
            else:
                bees_on_same_source = [b for b in self.colony if b.food_source == bee.food_source]
                probability_distribution = self.calculate_probabilities_for_onlookers(bees_on_same_source)
                lead_bee = choice(bees_on_same_source, 1, p=probability_distribution)[0]
                random_bee_index = bee.food_source

            bee.set_new_food_source_for_onlooker_bee(list(lead_bee.current_position), random_bee_index)

            if bee.fitness < lead_bee.fitness:
                lead_bee.current_position = list(bee.current_position)
                lead_bee.fitness = bee.fitness
                lead_bee.failures = 0
            else:
                lead_bee.failures += 1

    def scount_bees_exploration(self):
        employer_bees = [bee for bee in self.colony if bee.bee_type == BeeJob.EMPLOYED]
        probability_distribution = self.calculate_probabilities_for_onlookers(employer_bees)

        for bee in self.colony:
            assert len(bee.current_position) == self.dimensions
            if bee.failures > self.fail_limit:
                bee.current_position = self._get_random_positions()
                onlookers = [b for b in self.colony if bee.food_source == b.food_source]
                for b in onlookers:
                    lead_bee = choice(employer_bees, 1, p=probability_distribution)[0]
                    bee.set_new_food_source_for_onlooker_bee(list(lead_bee.current_position), lead_bee.food_source)

    def search(self):
        self.initialize_colony()
        self.evaluate_colony()
        self.update_best_solution()

        for i in range(self.max_iterations):
            self.employed_bees_exploration()
            self.onlooker_bees_exploration()
            self.scount_bees_exploration()
            self.evaluate_colony()
            self.update_best_solution()
            print(f"Best: {self.best_fitness}. Iteration: {i}")
            self.list_best_fitness.append(self.best_fitness)
        return self.list_best_fitness
