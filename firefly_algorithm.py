import random
import math

from particle import Particle
from parameters import num_of_individuos, dimensions, iterations_number


class Firefly():

	def __init__(self, function_wrapper):
		self.function = function_wrapper

	def search(self):
		bests = []
		self._initialize_particles()
		beta_inicial = 1
		light_rate = random.random()

		for iterations in range(iterations_number):
			for particle in self.population:
				particle.aply_function_on_current_position()

			population_cp = [particle.clone_particle() for particle in self.population]

			for particle_i in self.population:

				self._remove_matching_element_from_fireflies_copy(population_cp, particle_i)

				for particle_j in population_cp:
					if particle_i.fitness < particle_j.fitness:
						distance = self._euclidian_distance(particle_i, particle_j)
						beta = beta_inicial * math.exp(-1 * distance**2)

						for index in range(dimensions):
							new_location = particle_i.current_position[index] * (1 - beta) \
								+ particle_j.current_position[index] * beta \
								+ (random.random() - 0.5)
							new_location = self.__constrain_within_range(new_location, index)
							particle_i.current_position[index] = new_location

			bests.append(self._select_best_firefly_by_fitness(self.population).fitness)

		return bests

	def __constrain_within_range(self, new_location, index):
		if new_location < self.function.lower_bound:
			return self.function.lower_bound
		elif new_location > self.function.upper_bound:
			return self.function.upper_bound
		else:
			return new_location

	def _select_best_firefly_by_fitness(self, population):
		return min(population, key=lambda particle: particle.fitness)

	def _euclidian_distance(self, particle_i, particle_j):
		total = 0

		for i in range(dimensions):
			distance = (particle_i.current_position[i] - particle_j.current_position[i])**2
			total += distance
		return math.sqrt(total)

	def _remove_matching_element_from_fireflies_copy(self, fireflies_copy, firefly):
		matching_fireflies_copy_element = next((fireflies_copy_element for fireflies_copy_element in fireflies_copy if fireflies_copy_element.fitness == firefly.fitness), None)
		fireflies_copy.remove(matching_fireflies_copy_element)

	def _get_random_number(self):
		return (
			self.function.lower_bound + random.uniform(0, 1) * (self.function.upper_bound - self.function.lower_bound)
		)

	def _initialize_particles(self):
		self.population = []

		for i in range(num_of_individuos):
			random_position = [self._get_random_number() for index in range(dimensions)]
			particle = Particle(self.function, random_position)
			self.population.append(particle)
