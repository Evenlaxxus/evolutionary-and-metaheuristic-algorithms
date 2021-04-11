import itertools

import utils as utils
import numpy as np


def load(filename):
    return np.genfromtxt(filename, skip_header=6, skip_footer=1, dtype='int64')[:,1:]


def greedyLocalSearch(distances, type):
    number_of_all = distances.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))
    path, not_path = utils.make_random_path(number_of_half, number_of_all)
    actions = utils.swap_actions(number_of_half, type)
    result_of_itertools_product = itertools.product(np.arange(path.shape[0]), np.arange(not_path.shape[0]))
    exchange_actions = np.array(list(result_of_itertools_product), 'int')
    swapLen, exchangeLen = len(actions), len(exchange_actions)
    swapWithNoImprovement, exchangeWithNoImprovement = 0, 0
    np.random.shuffle(exchange_actions)
    np.random.shuffle(actions)

    while True:
        if swapLen <= swapWithNoImprovement and exchangeLen <= exchangeWithNoImprovement:
            break
        elif np.random.random() < 0.5 and swapLen > swapWithNoImprovement:
            action = actions[np.random.randint(len(actions)), :]
            delta = utils.calculate_swap_delta(action, path, distances, type)
            if delta > 0:
                utils.swap(path, action, type)
                swapWithNoImprovement = 0
            else:
                swapWithNoImprovement += 1
        else:
            exchange_action = actions[np.random.randint(len(actions)), :]
            delta = utils.calculate_exchange_delta(exchange_action, path, not_path, distances)
            if delta > 0:
                utils.exchange_vertices(path, not_path, exchange_action)
                exchangeWithNoImprovement = 0
            else:
                exchangeWithNoImprovement += 1
    return np.append(path, path[0])


if __name__ == '__main__':
    kroA100Data = utils.readTspFile("../data/kroA100.tsp")
    utils.localSearchTester(greedyLocalSearch, kroA100Data, "edges")
    utils.localSearchTester(greedyLocalSearch, kroA100Data, "vertices")
