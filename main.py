from firefly_algorithm import Firefly
from functions import Sphere, Rastrigin


def main():
	f = Firefly(Rastrigin())
	f.search()


main()