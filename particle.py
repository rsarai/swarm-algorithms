import numpy as np
import copy
import random
from parameters import dimensions, iterations_number
from enum import Enum

# np.random.seed(42)

class Particle():

    def __init__(self, function_wrapper, positions):
        self.function_wrapper = function_wrapper
        self.current_position = positions
        self.best_particle = self.current_position
        self.fitness = 1.0

    def aply_function_on_current_position(self):
        self.fitness = self.function_wrapper.calculate_fitness(self.current_position)

    def clone_particle(self):
        clone_object = copy.copy(self)
        clone_object.current_position = copy.deepcopy(self.current_position)
        clone_object.fitness = copy.deepcopy(self.fitness)
        return clone_object

class Fish():

    def __init__(self, objective_function, positions):
        self.fitness_function = objective_function
        self.current_position = positions
        self.weight = iterations_number / 2.0
        self.fitness = np.inf
        self.delta_fitness = 0
        self.delta_position = []

    def evaluate(self):
        new_fitness = self.fitness_function.calculate_fitness(self.current_position)
        self.fitness = new_fitness

    def update_position_individual_movement(self, step_ind):
        new_positions = []
        for pos in self.current_position:
            new = pos + (step_ind * np.random.uniform(-1, 1))
            if new > self.fitness_function.upper_bound:
                new = self.fitness_function.upper_bound
            elif new < self.fitness_function.lower_bound:
                new = self.fitness_function.lower_bound
            new_positions.append(new)
        assert len(new_positions) == len(self.current_position)

        new_fitness = self.fitness_function.calculate_fitness(new_positions)
        if new_fitness < self.fitness:
            self.delta_fitness = abs(new_fitness - self.fitness)
            self.fitness = new_fitness
            self.delta_position = [x - y for x, y in zip(new_positions, self.current_position)]
            self.current_position = list(new_positions)
        else:
            self.delta_position = [0] * dimensions
            self.delta_fitness = 0

    def feed(self, max_delta_fitness):
        if max_delta_fitness != 0:
            self.weight = self.weight + (self.delta_fitness / max_delta_fitness)
        else:
            self.weight = 1

    def update_position_collective_movement(self, sum_delta_fitness):
        collective_instinct = []
        for i, _ in enumerate(self.delta_position):
            collective_instinct.append(self.delta_position[i] * self.delta_fitness)
        if sum_delta_fitness != 0:
            collective_instinct = [val / sum_delta_fitness for val in collective_instinct]

        new_positions = []
        for i, _ in enumerate(self.current_position):
            new = self.current_position[i] + collective_instinct[i]
            if new > self.fitness_function.upper_bound:
                new = self.fitness_function.upper_bound
            elif new < self.fitness_function.lower_bound:
                new = self.fitness_function.lower_bound
            new_positions.append(new)

        assert len(new_positions) == len(self.current_position)
        self.current_position = list(new_positions)

    def update_position_volitive_movement(self, barycenter, step_vol, search_operator):
        new_positions = []
        for i, pos in enumerate(self.current_position):
            new = pos + (((pos - barycenter[i]) * step_vol * np.random.uniform(0, 1)) * search_operator)
            if new > self.fitness_function.upper_bound:
                new = self.fitness_function.upper_bound
            elif new < self.fitness_function.lower_bound:
                new = self.fitness_function.lower_bound
            new_positions.append(new)
        # volitive_step = [x - y for x, y in zip(self.current_position,barycenter)] / np.linalg.norm([self.current_position, barycenter])
        # volitive_step = np.random.uniform(0, 1) * step_vol * volitive_step * search_operator
        # new_positions = [x + y for x, y in zip(self.current_position, volitive_step)]

        assert len(new_positions) == len(self.current_position)
        self.current_position = list(new_positions)


class BeeJob(Enum):
    EMPLOYED = 1
    ONLOOKERS = 2
    SCOUT = 3


class Bee():

    def __init__(self, objective_function, positions, bee_type, food_source):
        self.objective_function = objective_function
        self.current_position = positions
        self.fitness = self._calculate_fitness(positions)
        self.bee_type = bee_type
        self.dimensions = 30  # hardcoded, but should be dimensions
        self.failures = 0
        self.food_source = food_source

    def evaluate(self):
        self.fitness = self._calculate_fitness(self.current_position)

    def employed_bees_explore_new_food_source(self, update=True):
        if self.bee_type == BeeJob.EMPLOYED:
            return

        if not update:
            return

        new_position = list(self.current_position)
        position2change = random.randint(0, self.dimensions - 1)
        random_index = self._get_random_number(position2change)
        new_pos = self.current_position[position2change] + random.uniform(-1, 1) * (self.current_position[position2change] - self.current_position[random_index])
        if new_pos > self.objective_function.upper_bound:
            new_pos = self.objective_function.upper_bound

        if new_pos < self.objective_function.lower_bound:
            new_pos = self.objective_function.lower_bound

        new_position[position2change] = new_pos
        new_fitness = self._calculate_fitness(new_position)
        if self.fitness < new_fitness:
            self.failures += 0
            return

        self.current_position = new_position
        self.fitness = new_fitness

    def set_new_food_source_for_onlooker_bee(self, source_position, food_source):
        new_position = list(self.current_position)
        position2change = random.randint(0, self.dimensions - 1)
        random_index = self._get_random_number(position2change)
        new_pos = self.current_position[position2change] + random.uniform(-1, 1) * (self.current_position[position2change] - source_position[random_index])
        if new_pos > self.objective_function.upper_bound:
            new_pos = self.objective_function.upper_bound

        if new_pos < self.objective_function.lower_bound:
            new_pos = self.objective_function.lower_bound

        new_position[position2change] = new_pos
        new_fitness = self._calculate_fitness(new_position)
        if self.fitness < new_fitness:
            return

        self.current_position = new_position
        self.food_source = food_source
        self.fitness = new_fitness

    def _calculate_fitness(self, new_position):
        return self.objective_function.calculate_fitness(new_position)

    def _get_random_number(self, excluded_index):
        random_index = random.randint(0, self.dimensions - 1)

        while random_index == excluded_index:
            random_index = random.randint(0, self.dimensions - 1)

        return random_index

    def set_position(self, new_positions):
        self.current_position = list(new_positions)
