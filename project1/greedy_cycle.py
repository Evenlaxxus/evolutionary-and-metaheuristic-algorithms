import math
import random

from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def readTspFile(filePath):
    tspFile = open(filePath)
    name = tspFile.readline().strip().split()[1]
    fileType = tspFile.readline().strip().split()[1]
    comment = tspFile.readline().strip().split()[1]
    dimension = tspFile.readline().strip().split()[1]
    edgeWeightType = tspFile.readline().strip().split()[1]
    tspFile.readline()

    nodeList = []
    n = int(dimension)
    for i in range(0, n):
        x, y = tspFile.readline().strip().split()[1:]
        nodeList.append([int(x), int(y)])
    return nodeList


def makeDistanceMatrix(vertexList):
    distanceMatrix = []
    for p in vertexList:
        distanceFromP = []
        for q in vertexList:
            distanceFromP.append(round(distance.euclidean(p, q)))
        distanceMatrix.append(distanceFromP)
    return distanceMatrix


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


def drawGraph(data, path):
    dataDict = {i: data[i] for i in range(0, len(data))}

    graph = nx.Graph()

    for i in dataDict:
        graph.add_node(i, pos=tuple(dataDict[i]))

    for i in range(len(path) - 1):
        graph.add_edge(path[i], path[i + 1])

    nx.draw_networkx_nodes(graph, dataDict)
    nx.draw_networkx_labels(graph, dataDict)
    nx.draw_networkx_edges(graph, dataDict)

    plt.show()
    plt.clf()


if __name__ == '__main__':
    kroA100Data = readTspFile("data/kroA100.tsp")
    kroB100Data = readTspFile("data/kroB100.tsp")

    kroA100 = GreedyCycle(makeDistanceMatrix(kroA100Data))
    kroB100 = GreedyCycle(makeDistanceMatrix(kroB100Data))

    drawGraph(kroA100Data, kroA100)
    drawGraph(kroB100Data, kroB100)
