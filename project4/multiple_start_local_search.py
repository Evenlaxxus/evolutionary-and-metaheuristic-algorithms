import time

import project3.candidate_local_search as steepest
import utils
import numpy as np


def testMultipleStartLocalSearch(testerRuns, algorithmRuns):
    data = utils.readTspFile("../data/kroA200.tsp")

    paths = []
    times = []
    for _ in range(testerRuns):
        start = time.time()
        paths.append(multipleStartLocalSearch(data, algorithmRuns))
        end = time.time()
        times.append(end - start)

    minRun = min(paths, key=lambda t: t[0])
    maxRun = max(paths, key=lambda t: t[0])

    distances = [p[0] for p in paths]
    averageDistance = sum(distances) / len(distances)

    minTime = min(times)
    maxTime = max(times)
    averageTime = sum(times) / len(times)

    print("minimalny dystans: " + str(minRun[0]), "średni dystans: " + str(averageDistance),
          "maksymalny dystans: " + str(maxRun[0]))
    print("minimalny czas: " + str(minTime), "maksymalny czas: " + str(maxTime),
          "średni czas: " + str(averageTime))

    utils.drawGraph(data, minRun[1])


def multipleStartLocalSearch(data, n):
    paths = []
    distanceMatrix = utils.makeDistanceMatrix(data)
    distances = np.array(utils.makeDistanceMatrix(data))

    for _ in range(n):
        paths.append(steepest.steepest(distances))

    distances = []
    for path in paths:
        distances.append(utils.calculatePathDistance(path, distanceMatrix))

    minDistance = min(distances)
    minPath = paths[distances.index(minDistance)]
    return minDistance, minPath


if __name__ == '__main__':
    testMultipleStartLocalSearch(10, 100)
