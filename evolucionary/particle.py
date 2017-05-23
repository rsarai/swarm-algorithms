import copy


class Particle():

	def __init__(self, function_wrapper, positions, strategy_parameters):
		self.function_wrapper = function_wrapper
		self.current_position = positions
		self.strategy_parameters = strategy_parameters
		self.best_particle = self.current_position
		self.fitness = 1.0

	def aply_function_on_current_position(self):
		self.fitness = self.function_wrapper.calculate_fitness(self.current_position)

	def clone_particle(self):
		clone_object = copy.copy(self)
		clone_object.current_position = copy.deepcopy(self.current_position)
		clone_object.fitness = copy.deepcopy(self.fitness)
		return clone_object
