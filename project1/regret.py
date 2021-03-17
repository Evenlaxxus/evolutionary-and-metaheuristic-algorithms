import math
import random

import utils


def Regret(distanceMatrix):
    startingVertex = random.randint(0, len(distanceMatrix) - 1)
    path = [startingVertex]
    for i in range(math.ceil(len(distanceMatrix) / 2)):
        vertexesCosts = []
        for item in range(len(distanceMatrix)):
            costList = []
            if item not in path:
                for n in range(len(path)):
                    distance1 = distanceMatrix[item][path[n - 1]]
                    distance2 = distanceMatrix[item][path[n]]
                    cost = distance1 + distance2 - distanceMatrix[path[n - 1]][path[n]]
                    costList.append((cost, n))
                costList = sorted(costList, key=lambda e: e[0])[0:3]
                vertexesCosts.append(
                    (item, costList[0][1], sum([costList[i][0] - costList[0][0] for i in range(len(costList))])))
        vertex, index, _ = max(vertexesCosts, key=lambda e: e[2])
        path.insert(index, vertex)
    path = path + [path[0]]
    return path


if __name__ == '__main__':
    kroA100Data = utils.readTspFile("data/kroA100.tsp")
    kroB100Data = utils.readTspFile("data/kroB100.tsp")

    kroA100 = Regret(utils.makeDistanceMatrix(kroA100Data))
    kroB100 = Regret(utils.makeDistanceMatrix(kroB100Data))

    utils.drawGraph(kroA100Data, kroA100)
    utils.drawGraph(kroB100Data, kroB100)
