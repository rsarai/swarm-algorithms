from firefly_algorithm import Firefly
from fish_school_search import FSS
from functions import Sphere, Rastrigin, Rosenbrocks
import matplotlib.pyplot as plt
import numpy as np


def main():
	# f = FSS(Rosenbrocks())
	# test = []
	# for i in range(3):
	# 	r = f.search()
	# 	test.append(r)
	# plt.boxplot(test, showfliers=False)
	# plt.show()

	f = FSS(Rosenbrocks())
	test = []
	print('Rosenbrocks')
	for i in range(30):
		print(i)
		r = f.search()
		test.append(r)

	soma = [0 for x in range(0,10000)]
	for i in range(0, 30):
	    for j in range(0, 10000):
	        new = soma[j] + test[i][j]
	        soma[j] = new

	soma = list(filter(lambda x: x/10000, soma))
	plt.plot(soma)
	plt.savefig('rosenbrocks.png')

def sphere():
	f = FSS(Sphere())
	test = []
	print('Sphere')
	for i in range(30):
		print(i)
		r = f.search()
		test.append(r)

	plt.boxplot(test, showfliers=False)
	plt.savefig('boxplot-sphere.png')

def rastrigin():
	f = FSS(Rastrigin())
	test = []
	print('Rastrigin')
	for i in range(30):
		print(i)
		r = f.search()
		test.append(r)
	plt.subplot(211)
	plt.boxplot(test, showfliers=False)

	soma = [0 for x in range(0,10000)]
	for i in range(0, 30):
	    for j in range(0, 10000):
	        new = soma[j] + test[i][j]
	        soma[j] = new

	soma = list(filter(lambda x: x/10000, soma))
	plt.subplot(212)
	plt.plot(soma)
	plt.savefig('fss-rastrigin.png')


rastrigin()
