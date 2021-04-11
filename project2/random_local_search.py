import numpy as np
import utils
import time


def load(filename):
    return np.genfromtxt(filename, skip_header=6, skip_footer=1, dtype='int64')[:,1:]


def random(distances, type):
    number_of_all = distances.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))

    timeout = 1   # [seconds]
    timeout_start = time.time()

    path, not_path = utils.make_random_path(number_of_half, number_of_all)
    shortest = utils.calculatePathDistance(path, distances)
    shortest_path = path

    while time.time() < timeout_start + timeout:
        path, not_path = utils.make_random_path(number_of_half, number_of_all)
        new_len = utils.calculatePathDistance(path, distances)
        if new_len < shortest:
            shortest = new_len
            shortest_path = path
    return shortest_path


def main():
    # instance = load(f'../data/kroA100.tsp')
    # distances = np.array(utils.makeDistanceMatrix(instance))
    # print(distances)
    # print(random(distances, "edges"))

    instance = load(f'../data/kroA100.tsp')
    kroA100Data = utils.readTspFile("../data/kroA100.tsp")
    utils.localSearchTester(random, kroA100Data, "vertices")


if __name__== "__main__":
    main()