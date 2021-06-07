import math
import time
import utils
import random
import numpy as np
from project3.candidate_local_search import steepest as candidate
from project2.steepest_local_search import steepest as steepest
from project3.list_of_moves import SteepestEdgeSwapListOfMoves, TSPReader

graph = TSPReader().read_graph_with_coords("../data/kroB200.tsp")

def evolutionaryTravelingSalesman(distanceMatrix, timeout):
    # city_list = [x for x in range(0, 200)]
    # population = make_populations(20, city_list)
    population = make_ls_populations(20, distanceMatrix)
    #print(population)
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        # two random parents
        parents = random.sample(population, k=2)
        #print(parents)
        # construct descendant
        descendant = recombination(parents)

        # local search

        fun = SteepestEdgeSwapListOfMoves(graph)
        function = fun.run
        #new = function()
        descendant = function(starting=descendant[:-1])
        descendant.append(descendant[0])
        descendantDistance = utils.calculatePathDistance(descendant, distanceMatrix)
        descendantDict = {
            "path": descendant,
            "length": descendantDistance
        }

        # steady state
        worst = population[0]
        for p in population:
            if p["length"] > worst["length"]:
                worst = p

        if worst["length"] > descendantDict["length"] and not isPathInPopulation(population, descendantDict["path"]):
            population.remove(worst)
            descendantDict["index"] = worst["index"]
            population.append(descendantDict)


    best_dist = population[0]["length"]
    best_path = population[0]["path"]
    # print(best_dist, best_path)
    for element in population:
        if element["length"] < best_dist:
            best_dist = element["length"]
            best_path = element["path"]
    # print(best_dist, best_path)

    return best_dist, best_path


def isPathInPopulation(population, path):
    for _ in range(len(path)):
        if any(np.array_equal(path, p) for p in population):
            return True
        path = path[1:] + [path[0]]
    return False


# def recombination(parents):
#     parent_1 = parents[0]
#     parent_2 = parents[1]
#     common = list(set(parent_1).intersection(parent_2))
#     combined = []
#     for i in range(len(parent_1["path"]) - 1):
#         if parent_1["path"][i] in common:
#             combined.append(parent_1["path"][i])
#         else:
#             choice = random.randint(0, 1)
#             if choice == 0 and parent_2["path"][i] not in common:
#                 combined.append(parent_2["path"][i])
#             else:
#                 combined.append(parent_1["path"][i])
#     return combined


def sequence_in_parents(parent_1, parent_2, i_a, i_b):
    first = -1
    while parent_1[i_a + first] == parent_2[i_b + first]:
        first -= 1
    first += 1

    last = 1
    while parent_1[(i_a + last) % len(parent_1)] == parent_2[(i_b + last) % len(parent_2)]:
        last += 1
    sequence = []
    i = first

    while i != last:
        sequence.append(parent_1[(i_a + i) % len(parent_1)])
        i += 1
    return sequence

def recombination(parents):
    parent_a = parents[0]["path"][:-1]
    parent_b = parents[1]["path"][:-1]
    #print(parent_a, parent_b)
    common_vertices = set(parent_a).intersection(set(parent_b))
    indexes_a = {v:i for i,v in enumerate(parent_a)}
    indexes_b = {v:i for i,v in enumerate(parent_b)}

    common_sequences = []
    number_of_nodes_in_common_sequences = 0
    not_available = set()
    while len(common_vertices) > 0:
        taken = common_vertices.pop()
        common_vertices.add(taken)
        index_from_1 = indexes_a[taken]
        index_from_2 = indexes_b[taken]
        sequence = sequence_in_parents(parent_a, parent_b, index_from_1, index_from_2)
        reverse_sequence = sequence_in_parents(parent_a, parent_b[::-1], index_from_1, (len(parent_b) - index_from_2 - 1))
        if len(sequence) < len(reverse_sequence):
            sequence = reverse_sequence
        for c in sequence:
            common_vertices.remove(c)

       # if len(com) > 1:
        number_of_nodes_in_common_sequences += len(sequence)
        common_sequences.append(sequence)
        for x in sequence:
            not_available.add(x)
    while number_of_nodes_in_common_sequences != len(parent_a):

        #x = parent_a[np.random.randint(len(parent_a))]
        if np.random.randn() < 0:
            x = np.random.choice(parent_a)
        else:
            x = np.random.choice(parent_b)

        if x not in not_available:
            common_sequences.append([x])
            number_of_nodes_in_common_sequences += 1
            not_available.add(x)

    np.random.shuffle(common_sequences)
    #commons.sort(key=lambda x: indexes_a[x[0]] if x[0] in indexes_a else indexes_b[x[0]])
    res = []

    for x in common_sequences:
        res.extend(x)

    return res


def createRoute(city_list):
    route = random.sample(city_list, math.ceil(len(city_list) / 2))
    return route


def make_populations(size, city_list, distanceMatrix):
    count = 0
    population = []
    while count < size:
        new = createRoute(city_list)
        if new not in population:
            population.append({
                "index": count,
                "path": new,
                "length": utils.calculatePathDistance(new, distanceMatrix)
            })
            count += 1
    return population

def make_ls_populations(size, distanceMatrix):
    count = 0
    population = []
    graph = TSPReader().read_graph_with_coords("../data/kroB200.tsp")
    fun = SteepestEdgeSwapListOfMoves(graph)
    while count < size:
        function = fun.run
        new = function()
        new.append(new[0])
        #new = steepest(np.array(distanceMatrix))
        if not isPathInPopulation(population, new):
            population.append({
                "index": count,
                "path": list(new),
                "length": utils.calculatePathDistance(new, distanceMatrix)
            })
            count += 1
    return population


def test_evolutionary(testerRuns, algorithmStopTime):
    data = utils.readTspFile("../data/kroB200.tsp")
    distanceMatrix = utils.makeDistanceMatrix(data)
    paths = []

    for _ in range(testerRuns):
        paths.append(evolutionaryTravelingSalesman(distanceMatrix, algorithmStopTime))

    minRun = min(paths, key=lambda t: t[0])
    maxRun = max(paths, key=lambda t: t[0])

    distances = [p[0] for p in paths]
    averageDistance = sum(distances) / len(distances)

    print("minimalny dystans: " + str(minRun[0]), "średni dystans: " + str(averageDistance),
          "maksymalny dystans: " + str(maxRun[0]))

    utils.drawGraph(data, minRun[1])


def main():
    # data = utils.readTspFile("../data/kroA200.tsp")
    # distanceMatrix = utils.makeDistanceMatrix(data)
    # evolutionaryTravelingSalesman(distanceMatrix, 15)
    test_evolutionary(10, 111)

if __name__ == '__main__':
    main()
