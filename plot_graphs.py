import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import operator


def plot_boxplot(best_fitness, description):
	fig1, ax1 = plt.subplots()
	ax1.set_title(description)
	ax1.boxplot(best_fitness, patch_artist=True, showfliers=False)
	ax1.legend()
	plt.savefig(f"{description}.png")


def plot_convergence_graphs(average_best_fitness, optimal, description):
    fig, ax = plt.subplots()
    ax.plot(list(range(0, 1000)), average_best_fitness, 'b', label=f"Optimal: {optimal}\n Best: {average_best_fitness[-1]:.2f}")
    ax.set_title(description)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Best Cost")
    ax.legend()
    plt.savefig(f'{description}.png')


def plot_path(points, path, description):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    # noinspection PyUnusedLocal
    y = list(map(operator.sub, [max(y) for i in range(len(points))], y))
    plt.plot(x, y, 'co')

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        # noinspection PyUnresolvedReferences
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

    # noinspection PyTypeChecker
    plt.xlim(0, max(x) * 1.1)
    # noinspection PyTypeChecker
    plt.ylim(0, max(y) * 1.1)
    plt.savefig(f'{description}.png')
