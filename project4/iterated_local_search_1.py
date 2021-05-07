import random
import sys
import time

import project3.candidate_local_search as steepest
import utils
import numpy as np


def testIteratedLocalSearch(testerRuns, algorithmStopTime):
    data = utils.readTspFile("../data/kroB200.tsp")

    paths = []

    for _ in range(testerRuns):
        paths.append(iteratedLocalSearch(data, algorithmStopTime))

    minRun = min(paths, key=lambda t: t[0])
    maxRun = max(paths, key=lambda t: t[0])

    distances = [p[0] for p in paths]
    averageDistance = sum(distances) / len(distances)

    print("minimalny dystans: " + str(minRun[0]), "średni dystans: " + str(averageDistance),
          "maksymalny dystans: " + str(maxRun[0]))

    utils.drawGraph(data, minRun[1])


def perturbate(path):
    v1 = random.choice(range(len(path)))

    indexes = list(range(len(path)))

    indexes.remove(v1)
    if v1 == len(path) - 1:
        indexes.remove(0)
    else:
        indexes.remove(v1 + 1)

    if v1 == 0:
        indexes.remove(len(path) - 1)
    else:
        indexes.remove(v1 - 1)

    v2 = random.choice(range(-len(path) + 3, -3))

    if v1 > v2:
        toFlip = np.append(path[v1:], path[:v2 + 1])
        toFlip = np.flip(toFlip)
        v1Len = len(path[v1:])
        path[v1:] = toFlip[:v1Len]
        path[:v2 + 1] = toFlip[v1Len:]
    else:
        path[v1:v2 + 1] = np.flip(path[v1:v2 + 1])
    return path


def perturbation(path, n):
    for _ in range(n):
        path = perturbate(path)
    return path


def iteratedLocalSearch(data, timeout):
    distanceMatrix = utils.makeDistanceMatrix(data)
    distances = np.array(utils.makeDistanceMatrix(data))

    timeout_start = time.time()
    minPath = steepest.steepest(distances)
    minDistance = utils.calculatePathDistance(minPath, distanceMatrix)
    while time.time() < timeout_start + timeout:
        path = perturbation(minPath, 4)
        path = steepest.steepest(distances, path)
        distance = utils.calculatePathDistance(path, distanceMatrix)
        if distance < minDistance:
            minDistance = distance
            minPath = path

    return minDistance, minPath


if __name__ == '__main__':
    testIteratedLocalSearch(10, 111)
