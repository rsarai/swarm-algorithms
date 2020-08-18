"""
The TSPLIB Symmetric Traveling Salesman Problem Instances
http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/
https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
"""
import random
import math
import numpy as np

from particle import Ant

# np.random.seed(42)
# random.seed(42)

class Graph:

    def __init__(self, cities):
        self.cities = cities
        self.pheromones = [[0.0 for _ in cities] for _ in cities]
        self.distance_matrix = [[]]
        self._create_distance_matrix()

    def _create_distance_matrix(self):
        self.distance_matrix = []
        for city in self.cities:
            row = []
            for other_city in self.cities:
                row.append(np.linalg.norm(np.array(city) - np.array(other_city)))
            self.distance_matrix.append(row)

class ACO:

    def __init__(self, graph, algorithm_type=1, rho_evaporation_rate=0.85, tour_counter=1000,
                 ants_count=30, alpha=1, beta=5, t_max=0.8, t_min=0.2):
        """
        :alpha: relative importance of pheromone
        :beta: relative importance of heuristic information
        :algorithm_type: 1 for regular ACO | 2 for MMACO
        """
        self.graph = graph
        self.town_count = len(graph.cities)
        self.tour_counter = tour_counter
        self.ants_count = ants_count
        self.alpha = alpha
        self.beta = beta
        self.rho_evaporation_rate = rho_evaporation_rate
        self.t_max = t_max
        self.t_min = t_min
        self.algorithm_type = algorithm_type

        self.best_solution = []
        self.best_cost = float("inf")
        self.best_cost_list = []
        self.all_ants = []

        if self.algorithm_type != 1:
            self.graph.pheromones = [[self.t_max for _ in self.graph.cities] for _ in self.graph.cities]

    def initialize_all_ants(self):
        self.all_ants = []
        for _ in range(self.ants_count):
            self.all_ants.append(
                Ant(current_town=random.randint(0, self.town_count - 1))
            )

    def construct_tour_for_each_ant(self):
        for _ in range(self.town_count - 1):
            for ant in self.all_ants:
                old_town = ant.current_town
                ant.move_next_city_to_construct_tour(self.graph, self.alpha, self.beta)
                assert old_town != ant.current_town

    def update_pheromone_trails(self):
        for ant in self.all_ants:
            ant.update_pheromone_trails(self.graph)

        for i, row in enumerate(self.graph.pheromones):
            for j, _ in enumerate(row):
                self.graph.pheromones[i][j] *= (1 - self.rho_evaporation_rate)

                if self.algorithm_type == 1:
                    for ant in self.all_ants:
                        self.graph.pheromones[i][j] += ant.pheromones_delta[i][j]
                else:
                    ant = self.get_best_ant_from_iteration()
                    self.graph.pheromones[i][j] += ant.pheromones_delta[i][j]
                    if self.graph.pheromones[i][j] > self.t_max:
                        self.graph.pheromones[i][j] = self.t_max
                    if self.graph.pheromones[i][j] < self.t_min:
                        self.graph.pheromones[i][j] = self.t_min

    def get_best_ant_from_iteration(self):
        best_ant = None
        best_distance = float('inf')
        for ant in self.all_ants:
            distance = ant.total_cost
            # distance = self.calculate_tour_distance(self.graph, ant.tabu_list)
            # assert distance == ant.total_cost
            if distance < best_distance:
                best_ant = ant
        return best_ant

    def update_best_solution(self):
        for ant in self.all_ants:
            ant.complet_tour_cost(self.graph)
            distance = ant.total_cost
            # distance = self.calculate_tour_distance(self.graph, ant.tabu_list)
            # assert round(distance, 5) == round(ant.total_cost, 5)
            if distance < self.best_cost:
                self.best_cost = distance
                self.best_solution = ant.tabu_list

    def search(self):
        for i in range(self.tour_counter):
            self.initialize_all_ants()
            self.construct_tour_for_each_ant()
            self.update_pheromone_trails()
            self.update_best_solution()
            print(f"Iteration {i}. Best cost: {self.best_cost}")
            self.best_cost_list.append(self.best_cost)
        return self.best_cost_list

    @classmethod
    def calculate_tour_distance(cls, graph, best_solution):
        result = 0
        for i in range(len(best_solution)):
            # result += math.sqrt((graph.cities[best_solution[i]][0] - graph.cities[best_solution[i - 1]][0])**2 + (graph.cities[best_solution[i]][1] - graph.cities[best_solution[i - 1]][1])**2)
            result += np.linalg.norm(np.array(graph.cities[best_solution[i]]) - np.array(graph.cities[best_solution[i - 1]]))
        return result
