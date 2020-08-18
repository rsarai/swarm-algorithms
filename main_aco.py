import numpy as np
import math
from aco import ACO, Graph
from plot_graphs import plot_path, plot_boxplot, plot_convergence_graphs


SIMULATIONS = 30


with open("data/att48.txt", "r") as f:
    matrix_cities = []
    for line in f.readlines():
        _, pos1, pos2 = line.split(" ")
        matrix_cities.append([float(pos1), float(pos2)])

with open("data/att48_optimal_tour.txt", "r") as f:
    best_solution = [int(line) for line in f.readlines()]
best_solution = [i - 1 for i in best_solution]

graph = Graph(cities=matrix_cities)
optimal = ACO.calculate_tour_distance(graph, best_solution)


best_fitness = []
for _ in range(SIMULATIONS):
    aco = ACO(graph=graph, algorithm_type=1, rho_evaporation_rate=0.9)
    best_cost_list = aco.search()
    best_fitness.append(best_cost_list)
    print("Optimal: ", optimal)
    print("Found: ", ACO.calculate_tour_distance(graph, aco.best_solution))
print("ACO Min: ", np.array(best_fitness).min())

# plot_boxplot(best_fitness, "Boxplot ACO Average 30 Runs")
# average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS

# plot_path(graph.cities, aco.best_solution, "ACO Found Solution")
# plot_convergence_graphs(average_best_fitness, optimal, "ACO Convergence Average 30 Runs")


best_fitness = []
for _ in range(SIMULATIONS):
    aco = ACO(graph=graph, algorithm_type=2, rho_evaporation_rate=0.9)
    best_cost_list = aco.search()
    best_fitness.append(best_cost_list)
    print("Optimal: ", optimal)
    print("Found: ", ACO.calculate_tour_distance(graph, aco.best_solution))
    print(aco.best_solution)
print("MMACO Min: ", np.array(best_fitness).min())


# plot_boxplot(best_fitness, "Boxplot MMACO Average 30 Runs")
# average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS

# plot_path(graph.cities, aco.best_solution, "MMACO Found Solution")
# plot_convergence_graphs(average_best_fitness, optimal, "MMACO Convergence Average 30 Runs")


# total_distance = 0
# for i in range(len(best_solution)):
#     total_distance += np.linalg.norm(
#         np.array(matrix_cities[best_solution[i]]) - np.array(matrix_cities[best_solution[i - 1]])
#     )
# print(total_distance)


# result = 0
# result_2 = 0
# for i in range(len(best_solution)):
#     # partial_result = math.sqrt((graph.cities[best_solution[i]][0] - graph.cities[best_solution[i - 1]][0])**2 + (graph.cities[best_solution[i]][1] - graph.cities[best_solution[i - 1]][1])**2)
#     partial_result = np.linalg.norm(np.array(graph.cities[best_solution[i]]) - np.array(graph.cities[best_solution[i - 1]]))
#     partial_result_2 = graph.distance_matrix[best_solution[i]][best_solution[i - 1]]
#     assert partial_result == partial_result_2
#     result += partial_result
#     result_2 += partial_result_2

# print(result)
# print(result_2)
