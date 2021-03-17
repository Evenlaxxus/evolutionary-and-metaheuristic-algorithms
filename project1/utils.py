import random

from scipy.spatial import distance
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


def drawGraph(data, path):
    dataDict = {i: data[i] for i in range(0, len(data))}

    graph = nx.Graph()

    for i in dataDict:
        graph.add_node(i, pos=tuple(dataDict[i]))

    for i in range(len(path) - 1):
        graph.add_edge(path[i], path[i + 1])

    nx.draw_networkx(graph, pos=dataDict, font_size=6, node_size=50)

    plt.show()
    plt.clf()


def calculatePathDistance(path, distanceMatrix):
    pathDistance = 0
    for vertex in range(len(path) - 1):
        pathDistance += distanceMatrix[path[vertex]][path[vertex + 1]]
    return pathDistance


def tester(function, data):
    startingVertexes = random.sample(range(100), 50)
    distanceMatrix = makeDistanceMatrix(data)

    paths = []
    for vertex in startingVertexes:
        paths.append(function(distanceMatrix, vertex))
    distances = []
    for path in paths:
        distances.append(calculatePathDistance(path, distanceMatrix))

    minDistance = min(distances)
    minPath = paths[distances.index(minDistance)]
    maxDistance = max(distances)
    maxPath = paths[distances.index(maxDistance)]
    averageDistance = sum(distances) / len(distances)

    print("minimalny dystans: " + str(minDistance), "maksymalny dystans: " + str(maxDistance),
          "średni dystans: " + str(averageDistance))

    drawGraph(data, minPath)
    drawGraph(data, maxPath)
