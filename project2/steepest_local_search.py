import itertools
import numpy as np
import utils
from scipy.spatial import distance


def make_random_path(length, size):
    points = np.arange(size)
    np.random.shuffle(points)
    path, not_path = points[:length], points[length:]
    return path, not_path


def swap(path, vertices, type):
    if type == "edges":
        v1, v2 = vertices
        path[v1:v2 + 1] = np.flip(path[v1:v2 + 1])
    elif type == "vertices":
        v1, v2 = vertices
        path[v1], path[v2] = path[v2], path[v1]


def exchange_vertices(path, not_path, exchange_action):
    vp, vo = exchange_action
    path[vp], not_path[vo] = not_path[vo], path[vp]


def swap_actions(path_length, type):
    if type == "vertices":
        return np.array(list(itertools.combinations(np.arange(path_length), 2)), 'int')
    elif type == "edges":
        combinations = itertools.combinations(np.arange(path_length), 2)
        return np.array([[v1, v2] for v1, v2 in combinations if 1 < v2 - v1 < path_length - 1], 'int')


def calculate_swap_delta(swap_action, path, distances, type):
    if type == "vertices":
        p1, p2 = swap_action
        before = distances[path[p1], path[p1 - 1]] + distances[path[p2], path[p2 - 1]] + \
              distances[path[p1], path[(p1 + 1) % len(path)]] + distances[path[p2], path[(p2 + 1) % len(path)]]
        after = distances[path[p2], path[p1 - 1]] + distances[path[p1], path[p2 - 1]] + \
              distances[path[p2], path[(p1 + 1) % len(path)]] + distances[path[p1], path[(p2 + 1) % len(path)]]
        if abs(p1 - p2) == 1 or abs(p1 - p2) == len(path) - 1:
            after += (distances[path[p1], path[p2]]) * 2
        return before - after
    elif type == "edges":
        v1, v2 = swap_action
        v1_prev = v1 - 1
        v2_next = (v2 + 1) % len(path)
        before = distances[path[v1_prev], path[v1]] + distances[path[v2], path[v2_next]]
        after = distances[path[v1_prev], path[v2]] + distances[path[v1], path[v2_next]]
        return before - after


def calculate_exchange_delta(exchange_action, path, not_path, distances):
    in_path, out_of_path = exchange_action
    before = distances[path[in_path], path[in_path - 1]] + distances[path[in_path], path[(in_path + 1) % len(path)]]
    after = distances[not_path[out_of_path], path[in_path - 1]] + distances[not_path[out_of_path], path[(in_path + 1) % len(path)]]
    return before - after


def load(filename):
    return np.genfromtxt(filename, skip_header=6, skip_footer=1, dtype='int64')[:,1:]


def steepest(distances, type):
    number_of_all = distances.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))
    path, not_path = make_random_path(number_of_half, number_of_all)
    actions = swap_actions(number_of_half, type)
    result_of_itertools_product = itertools.product(np.arange(path.shape[0]), np.arange(not_path.shape[0]))
    exchange_actions = np.array(list(result_of_itertools_product), 'int')

    while True:
        swap_delta = [calculate_swap_delta(one_swap, path, distances, type) for one_swap in actions]
        exchange_delta = [calculate_exchange_delta(one_exchange, path, not_path, distances) for one_exchange in exchange_actions]
        id_max_swap = int(np.argmax(swap_delta))
        id_exchange_max = int(np.argmax(exchange_delta))
        max_swap = swap_delta[id_max_swap]
        max_exchange = exchange_delta[id_exchange_max]
        if max_swap <= 0 and max_exchange <= 0:
            break
        if max_swap > max_exchange:
            swap(path, actions[id_max_swap], type)
        else:
            exchange_vertices(path, not_path, exchange_actions[id_exchange_max])
    return path


def main():
    instance = load(f'data/kroA100.tsp')
    kroA100Data = utils.readTspFile("data/kroA100.tsp")
    distances = np.array(utils.makeDistanceMatrix(instance))
    print(distances)
    result_path = list(steepest(distances, "edges"))
    result_path.append(result_path[0])
    print(result_path)
    utils.drawGraph(kroA100Data, result_path)


if __name__== "__main__":
    main()