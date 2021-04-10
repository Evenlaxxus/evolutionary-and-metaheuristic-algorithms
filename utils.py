import random
import itertools

from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time


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


def localSearchTester(function, data, mode):
    distanceMatrix = makeDistanceMatrix(data)
    distances = np.array(makeDistanceMatrix(data))

    paths = []
    times = []
    for _ in range(100):
        start = time.time()
        paths.append(function(distances, mode))
        end = time.time()
        times.append(end - start)

    distances = []
    for path in paths:
        distances.append(calculatePathDistance(path, distanceMatrix))

    minDistance = min(distances)
    minPath = paths[distances.index(minDistance)]
    maxDistance = max(distances)
    maxPath = paths[distances.index(maxDistance)]
    averageDistance = sum(distances) / len(distances)
    minTime = min(times)
    maxTime = max(times)
    averageTime = sum(times) / len(times)

    print("minimalny dystans: " + str(minDistance), "maksymalny dystans: " + str(maxDistance),
          "średni dystans: " + str(averageDistance))
    print("minimalny czas: " + str(minTime), "maksymalny czas: " + str(maxTime),
          "średni czas: " + str(averageTime))

    drawGraph(data, minPath)
    drawGraph(data, maxPath)
