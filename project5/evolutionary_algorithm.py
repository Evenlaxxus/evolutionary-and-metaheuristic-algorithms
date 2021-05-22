import math
import time
import utils
import random
import numpy as np
from project3.candidate_local_search import steepest


def evolutionaryTravelingSalesman(distanceMatrix, timeout):
    city_list = [x for x in range(0, 200)]
    population = make_populations(20, city_list, distanceMatrix)

    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        # two random parents
        parents = random.sample(population, k=2)

        # construct descendant
        descendant = recombination(parents)

        # local search
        descendant = steepest(np.array(distanceMatrix), descendant)
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
    print(population)


def isPathInPopulation(population, path):
    for _ in range(len(path)):
        if any(np.array_equal(path, p) for p in population):
            return True
        path = path[1:] + [path[0]]
    return False


def recombination(parents):
    parent_1 = parents[0]
    parent_2 = parents[1]
    common = list(set(parent_1).intersection(parent_2))
    combined = []
    for i in range(len(parent_1["path"])):
        if parent_1["path"][i] in common:
            combined.append(parent_1["path"][i])
        else:
            choice = random.randint(0, 1)
            if choice == 0 and parent_2["path"][i] not in common:
                combined.append(parent_2["path"][i])
            else:
                combined.append(parent_1["path"][i])
    return combined


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


def main():
    data = utils.readTspFile("../data/kroA200.tsp")
    distanceMatrix = utils.makeDistanceMatrix(data)
    evolutionaryTravelingSalesman(distanceMatrix, 15)


if __name__ == '__main__':
    main()
