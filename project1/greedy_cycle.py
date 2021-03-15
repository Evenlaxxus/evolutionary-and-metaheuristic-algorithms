import math
import random

import numpy as np
import utils


def GreedyCycle(distanceMatrix):
    startingVertex = random.randint(0, len(distanceMatrix) - 1)
    path = [startingVertex]
    for i in range(math.ceil(len(distanceMatrix) / 2)):
        minCost = np.uint64(-1)
        minCostIndex = -1
        vertexToAdd = -1
        for j, item in enumerate(range(len(distanceMatrix))):
            if item not in path:
                for n in range(len(path)):
                    distance1 = distanceMatrix[item][path[n - 1]]
                    distance2 = distanceMatrix[item][path[n]]
                    cost = distance1 + distance2 - distanceMatrix[path[n - 1]][path[n]]

                    if cost < minCost:
                        minCostIndex = n
                        vertexToAdd = item
                        minCost = cost
        path.insert(minCostIndex, vertexToAdd)
    path = path + [path[0]]

    return path


if __name__ == '__main__':
    kroA100Data = utils.readTspFile("data/kroA100.tsp")
    kroB100Data = utils.readTspFile("data/kroB100.tsp")

    kroA100 = GreedyCycle(utils.makeDistanceMatrix(kroA100Data))
    kroB100 = GreedyCycle(utils.makeDistanceMatrix(kroB100Data))

    utils.drawGraph(kroA100Data, kroA100)
    utils.drawGraph(kroB100Data, kroB100)
