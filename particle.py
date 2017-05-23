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

	def __init__(self, function_wrapper, positions, weights):
		self.function_wrapper = function_wrapper
		self.current_position = positions
		self.previous_position = positions
		self.best_particle = self.current_position
		self.fitness = 1.0
		self.weights = weights
		self.previous_weight = 0
		self.indivial_step = [0.10, 0.0001, 0.10, 0.0001, 0.10, 0.0001, 0.10, 0.0001, 0.10, 0.0001,0.10, 0.0001,0.10, 0.0001,0.10, 0.0001, 0.10, 0.0001,0.10, 0.0001,0.10, 0.0001,0.10, 0.0001,0.10, 0.0001,0.10, 0.0001,0.10, 0.0001]

	def aply_function_on_current_position(self):
		self.fitness = self.function_wrapper.calculate_fitness(self.current_position)

	def individual_movement(self):
		new_position = []
		for i in range(0, len(self.current_position)):
			new_position.append(self.current_position[i] + self.indivial_step[i] * random.uniform(-1, 1))
		return new_position


	def clone_particle(self):
		clone_object = copy.copy(self)
		clone_object.current_position = copy.deepcopy(self.current_position)
		clone_object.fitness = copy.deepcopy(self.fitness)
		return clone_object


class Bee():

	def __init__(self, function_wrapper, positions):
		self.function_wrapper = function_wrapper
		self.current_position = positions
		self.best_particle = self.current_position
		self.fitness = 1.0
