from firefly_algorithm import Firefly
from fish_school_search import FSS
from functions import Sphere, Rastrigin, Rosenbrocks
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from parameters import iterations_number

SIMULATIONS = 1

np.random.seed(42)

def rosenbrocks():
	print('Rosenbrocks')

	best_fitness = []
	for _ in range(SIMULATIONS):
		fss = FSS(Rosenbrocks())
		fss.search()
		best_fitness.append(fss.list_global_best_values)

	average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
	plot_graphs(average_best_fitness, "Rosenbrocks")
	plot_boxplot(best_fitness, "Rosenbrocks")


def plot_boxplot(best_fitness, function_name):
	fig1, ax1 = plt.subplots()
	ax1.set_title(f'BoxPlot Best Fitness for {function_name}')
	ax1.boxplot(best_fitness, patch_artist=True)
	ax1.legend()
	plt.savefig(f'FSS Boxplot {function_name}.png')


def plot_graphs(average_best_fitness, function_name):

    mpl.style.use('seaborn')

    fig, ax = plt.subplots()
    ax.plot(list(range(0, iterations_number)), average_best_fitness, 'b', label=f"Best: {average_best_fitness[-1]:.2f}")
    ax.set_title(f"FSS {function_name}: Average {SIMULATIONS} runs")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Best Fitness")
    ax.legend()
    plt.savefig(f'FSS Convergence {function_name}.png')


def rastrigin():
	print('Rastrigin')

	best_fitness = []
	for _ in range(SIMULATIONS):
		fss = FSS(Rastrigin())
		fss.search()
		best_fitness.append(fss.list_global_best_values)

	average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
	plot_graphs(average_best_fitness, "Rastrigin")
	plot_boxplot(best_fitness, "Rastrigin")


def sphere():
	print('sphere')

	best_fitness = []
	for _ in range(SIMULATIONS):
		fss = FSS(Sphere())
		fss.search()
		best_fitness.append(fss.list_global_best_values)

	average_best_fitness = np.sum(np.array(best_fitness), axis=0) / SIMULATIONS
	plot_graphs(average_best_fitness, "Sphere")
	plot_boxplot(best_fitness, "Sphere")


# sphere()
# rosenbrocks()
rastrigin()
