import numpy as np
import copy
import random


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
        self.weight = 1.0
        self.fitness = np.inf
        self.delta_fitness = 0
        self.delta_position = []

    def evaluate(self):
        new_fitness = self.fitness_function.calculate_fitness(self.current_position)
        self.fitness = new_fitness

    def update_position_individual_movement(self, step_ind):
        new_positions = [pos + step_ind * random.uniform(-1, 1) for pos in self.current_position]
        assert len(new_positions) == len(self.current_position)
        self.delta_position = [x - y for x, y in zip(self.current_position, new_positions)]
        self.current_position = list(new_positions)

        old_fitness = self.fitness
        self.evaluate()
        self.delta_fitness = old_fitness - self.fitness

    def feed(self, max_delta_fitness):
        self.weight = self.weight + self.delta_fitness / max_delta_fitness

    def update_position_collective_movement(self, sum_delta_fitness):
        collective_instinct = sum([pos * self.delta_fitness for pos in self.delta_position]) / sum_delta_fitness
        import pdb; pdb.set_trace()
        new_positions = [pos + collective_instinct for pos in self.current_position]
        assert len(new_positions) == len(self.current_position)

        self.delta_position = [x - y for x, y in zip(self.current_position, new_positions)]
        self.current_position = list(new_positions)

    def update_position_volitive_movement(self, barycenter, step_vol, search_operator):
        volitive_step = [x - y for x, y in zip(self.current_position,barycenter)] / np.linalg.norm([self.current_position, barycenter])
        volitive_step = random.uniform(0.1, 0.9) * step_vol * volitive_step * search_operator

        new_positions = [x + y for x, y in zip(self.current_position, volitive_step)]
        assert len(new_positions) == len(self.current_position)

        self.delta_position = [x - y for x, y in zip(self.current_position, new_positions)]
        self.current_position = list(new_positions)


class Bee():

    def __init__(self, function_wrapper, positions):
        self.function_wrapper = function_wrapper
        self.current_position = positions
        self.best_particle = self.current_position
        self.fitness = 1.0
