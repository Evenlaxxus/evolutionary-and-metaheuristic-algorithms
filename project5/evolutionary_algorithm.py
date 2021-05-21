import time
import utils
from project3.candidate_local_search import steepest


def evolutionaryTravelingSalesman(distanceMatrix, timeout):
    population = []

    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        # two random parents
        parents = []

        # construct descendant
        descendant = recombination(parents)

        # local search
        descendant = steepest(distanceMatrix, descendant)
        descendantDistance = utils.calculatePathDistance(descendant, distanceMatrix)

        # steady state
        worstPath = population[0]
        worstDistance = utils.calculatePathDistance(population[0], distanceMatrix)
        for path in population:
            distance = utils.calculatePathDistance(path, distanceMatrix)
            if distance > worstDistance:
                worstDistance = distance
                worstPath = path

        # TODO replace descendant not in population with something better
        if worstDistance > descendantDistance and descendant not in population:
            population.remove(worstPath)
            population.append(descendant)


def recombination(parents):
    return []
