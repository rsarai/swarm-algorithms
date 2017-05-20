import copy
import functools
import random
import math

from fish import Fish
from parameters import num_of_individuos, dimensions, iterations_number


class FSS():

    def __init__(self, function_wrapper):
        self.function = function_wrapper

    def search(self):
        bests = []
        maximum_weight_value = 1000
        individual_step_dacay = 0.00005
        self._initialize_particles()

        for iterations in range(iterations_number):

            # individual_movement
            fitness_variations = []
            for fish in self.population:
                new_position = fish.individual_movement()
                new_fish = Fish(fish.function_wrapper, new_position, fish.weights)
                new_fish.aply_function_on_current_position()
                fish.aply_function_on_current_position()

                if new_fish.fitness < fish.fitness:
                    new_fish.previous_position = fish.current_position
                    fish = new_fish
                else:
                    fish.previous_position = fish.current_position

                fitness_variations.append(abs(new_fish.fitness - fish.fitness))

            # feed fishes
            max_variation = max(fitness_variations)
            for fish in self.population:
                new_weight = fish.weights + (fish.fitness / max_variation)
                fish.previous_weight = fish.weights
                fish.weights = new_weight
                if fish.weights > maximum_weight_value:
                    fish.weights = maximum_weight_value

            # calculates vector of instintict moviments
            distance_variations_sum = [0 for i in range(0, dimensions)]
            fitness_variations_sum = sum(fitness_variations)
            for fish in self.population:

                for i in range(0, dimensions):
                    distance_variations = abs(fish.current_position[i] - fish.previous_position[i])
                    distance_variations_sum[i] = distance_variations_sum[i] + (distance_variations * fitness_variations[i])

            instintive_movement_array = []
            for i in range(0, dimensions):
                if fitness_variations_sum != 0:
                    instintive_movement_array.append(distance_variations_sum[i]/fitness_variations_sum)
                else:
                    instintive_movement_array.append(0)

            # executes instintive moviments
            for fish in self.population:
                for i in range(0, dimensions):
                    fish.current_position[i] = fish.current_position[i] + instintive_movement_array[i]

            # calculates the baricenter
            weights_sum = 0
            for fish in  self.population:
                weights_sum = fish.weights

            weights_sum_times_position = 0
            for fish in self.population:
                for i in range(0, dimensions):
                    weights_sum_times_position = weights_sum_times_position + (fish.current_position[i] * fish.weights)

            baricenter = [weights_sum_times_position / weights_sum for i in range(0, dimensions)]

            # executes volitive moviment
            for fish in self.population:
                distance_to_baricenter = self._euclidian_distance(fish.current_position, baricenter)

                volational_array = []
                difference_to_baricenter = []
                weight_variation_sum = 0
                for i in range(0, dimensions):
                    volational_array.append(2 * fish.current_position[i])
                    difference_to_baricenter.append(fish.current_position[i] - baricenter[i])
                    weight_variation_sum = weight_variation_sum + abs(fish.weights - fish.previous_weight)

                sign = functools.partial(math.copysign, 1)
                for i in range(0, dimensions):
                    fish.current_position[i] = fish.current_position[i] + -sign(weight_variation_sum) * volational_array[i] * random.random() * difference_to_baricenter[i] / distance_to_baricenter

            for fish in self.population:
                for i in range(0, dimensions):
                    fish.current_position[i] -= individual_step_dacay

            for fish in self.population:
                fish.aply_function_on_current_position()

            bests.append(min([fish.fitness for fish in self.population]))
        return bests


    def _initialize_particles(self):
        self.population = []
        for i in range(num_of_individuos):
            random_position = [self._get_random_number() for index in range(dimensions)]
            fish = Fish(self.function, random_position, random.uniform(300, 600))
            self.population.append(fish)

    def _euclidian_distance(self, particle_i, particle_j):
        total = 0
        for i in range(dimensions):
            distance = (particle_i[i] - particle_j[i])**2
            total += distance
        return math.sqrt(total)

    def _get_random_number(self):
        return (
            self.function.lower_bound + random.uniform(0, 1) * (self.function.upper_bound - self.function.lower_bound)
        )
