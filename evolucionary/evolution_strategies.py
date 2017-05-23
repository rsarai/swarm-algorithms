import random
import math
import copy

from functions import Sphere
from particle import Particle
from parameters import num_of_individuos, dimensions, iterations_number, number_of_offspring
#  u -> num_of_individuos / parental population size


class ES():

	def __init__(self, function_wrapper):
		self.function = function_wrapper

	def search(self):
		self._initialize_population()

		for iterations in range(iterations_number):
			for particle in self.population:
				particle.aply_function_on_current_position()

			for i in range(0, number_of_offspring):
				parents = self._select_random_parents()
				offspring = self._crossover_operator(parents)
				new_individuo = self.mutate_offspring(offspring)
				new_individuo.aply_function_on_current_position()
				self.population.append(new_individuo)
			# no nosso caso o melhor
			best = self.select_bests_for_population()
			self.population = []
			self.population.append(best)

	def select_bests_for_population(self):
		best = min(self.population, key = lambda individuo : individuo.fitness)
		return best

	def _initialize_population(self):
		self.population = []
		for i in range(num_of_individuos):
			random_position = [self._get_random_number() for index in range(dimensions)]
			random_strategies = [random.random() for index in range(dimensions)]
			p = Particle(self.function, random_position, random_strategies)
			self.population.append(p)

	def _get_random_number(self):
		return (
			self.function.lower_bound + random.uniform(0, 1) * (self.function.upper_bound - self.function.lower_bound)
		)

	def _select_random_parents(self):
		if num_of_individuos < 2:
			return [self.population[0], self.population[0]]
		else:
			rand = random.randint(len(self.population))
			new_pop = copy.deepcopy(self.population)
			new_pop.remove(self.population[rand])
			rand2 = random.randint(len(new_pop))
			return [self.population[rand], new_pop[rand2]]

	# Create offspring through application of crossover operator on parent genotypes and strategy parameters;
	def _crossover_operator(self, parents):
		# simples
		position = []
		strategy = []
		parent1 = parents[0]
		parent2 = parents[1]
		for i in range(dimensions):
			if random.random() > 0.5:
				position.append(parent2.current_position[i])
				strategy.append(parent2.strategy_parameters[i])
			else:
				position.append(parent1.current_position[i])
				strategy.append(parent1.strategy_parameters[i])
		offspring = Particle(self.function, position, strategy)
		return offspring

	def mutate_offspring(self, offspring):
		current_position = []
		strategy_parameters = []
		for i in range(dimensions):
			current_position.append(self.mutation(offspring.current_position[i], offspring.strategy_parameters[i]))
			strategy_parameters.append(self.adapt_stepsize())
		new_individuo = Particle(self.function, current_position, strategy_parameters)
		return new_individuo

	def mutation(self, value, q):
		rand = -1 if random.random() < 0.5 else 1
		return value + rand*self.gauss(q)

	def gauss(self, q):
		x = random.random() * q * 3
		n = (1.0 / math.sqrt(q * q * math.pi)) * math.exp((x * x / q * q) * (-1 / 2))
		return n
#
# 	# def crossover_local_intermediare_recombination(parents):
# 	# 	r = random.random()
# 	# 	new_position = []
# 	# 	for i in range(len(parents.current_position)):
#
	def adapt_stepsize(self):
		pass
#     #     if self.adap in ['1/5th','1/5th-rule','1/5-Erfolgsregel','Erfolgsregel']:
#     #         improv=0
#     #         for fdude in self.F1:
#     #             if fdude.isbetter(self.F0[0]): improv+=1
#     #         if improv > self.l/5:  # alternative: if improv > self.l/5+1
#     #             self.mstep*=self.adapf
#     #         else:
#     #             self.mstep/=self.adapf
#     #     elif self.adap in ['const','const.','constant']:
# 	# 		pass
#
# 	# def mutate_fixstep(self,stepsize=None,uCS=True,mirrorbds=True):
#     #     # mutation as jump into a random direction with fixed step size
#     #     if stepsize is None: stepsize=self.mstep
#     #     step=randn(self.ng); step=stepsize*step/sqrt(np.sum(step*step))
#     #     if uCS:
#     #         DNA=self.get_uDNA(); DNA+=step; self.set_uDNA(DNA)
#     #     else:
# 	# 		self.DNA+=step
#
#
r = ES(Sphere())
r.search()
