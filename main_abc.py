from functions import Rastrigin
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from parameters import iterations_number
from abcolony import ABC
from enum import Enum

mpl.style.use('seaborn')

SIMULATIONS = 30

class POSITION_UPDATE(Enum):
    TRADITIONAL = 1
    FOOD_SOURCE = 2
    PROBABILITY = 3


def plot_boxplot(best_fitness, function_name):
	fig1, ax1 = plt.subplots()
	ax1.set_title(f'BoxPlot Best Fitness for {function_name}')
	ax1.boxplot(best_fitness, patch_artist=True, showfliers=False)
	ax1.legend()
	plt.savefig(f'ABC Boxplot {function_name}.png')


def plot_graphs(average_best_fitness, function_name):
    fig, ax = plt.subplots()
    ax.plot(list(range(0, iterations_number)), average_best_fitness, 'b', label=f"Best: {average_best_fitness[-1]:.2f}")
    ax.set_title(f"ABC {function_name}: Average {SIMULATIONS} runs")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Best Fitness")
    ax.legend()
    plt.savefig(f'ABC Convergence {function_name}.png')


print('Rastrigin')
# best_fitness = []

# for _ in range(SIMULATIONS):
#     abc = ABC(POSITION_UPDATE.TRADITIONAL)
#     results = abc.search()
#     best_fitness.append(results)

# plot_boxplot(best_fitness, "Rastrigin (Traditional)")
# average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
# plot_graphs(average_best_fitness, "Rastrigin (Traditional)")


# best_fitness = []

# for _ in range(SIMULATIONS):
#     abc = ABC(POSITION_UPDATE.FOOD_SOURCE)
#     results = abc.search()
#     best_fitness.append(results)

# plot_boxplot(best_fitness, "Rastrigin (Food Source)")
# average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
# plot_graphs(average_best_fitness, "Rastrigin (Food Source)")


# best_fitness = []
# for _ in range(SIMULATIONS):
#     abc = ABC(POSITION_UPDATE.PROBABILITY)
#     results = abc.search()
#     best_fitness.append(results)

# plot_boxplot(best_fitness, "Rastrigin (Probability)")
# average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
# plot_graphs(average_best_fitness, "Rastrigin (Probability)")

