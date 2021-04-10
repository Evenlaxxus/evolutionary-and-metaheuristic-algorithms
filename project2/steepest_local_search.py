import itertools
import numpy as np
import utils


def load(filename):
    return np.genfromtxt(filename, skip_header=6, skip_footer=1, dtype='int64')[:, 1:]


def steepest(distances, type):
    number_of_all = distances.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))
    path, not_path = utils.make_random_path(number_of_half, number_of_all)
    actions = utils.swap_actions(number_of_half, type)
    result_of_itertools_product = itertools.product(np.arange(path.shape[0]), np.arange(not_path.shape[0]))
    exchange_actions = np.array(list(result_of_itertools_product), 'int')

    while True:
        swap_delta = [utils.calculate_swap_delta(one_swap, path, distances, type) for one_swap in actions]
        exchange_delta = [utils.calculate_exchange_delta(one_exchange, path, not_path, distances) for one_exchange in
                          exchange_actions]
        id_max_swap = int(np.argmax(swap_delta))
        id_exchange_max = int(np.argmax(exchange_delta))
        max_swap = swap_delta[id_max_swap]
        max_exchange = exchange_delta[id_exchange_max]
        if max_swap <= 0 and max_exchange <= 0:
            break
        if max_swap > max_exchange:
            utils.swap(path, actions[id_max_swap], type)
        else:
            utils.exchange_vertices(path, not_path, exchange_actions[id_exchange_max])
    return np.append(path, path[0])


def main():
    kroA100Data = utils.readTspFile("../data/kroA100.tsp")
    utils.localSearchTester(steepest, kroA100Data, "edges")
    utils.localSearchTester(steepest, kroA100Data, "vertices")


if __name__ == "__main__":
    main()
