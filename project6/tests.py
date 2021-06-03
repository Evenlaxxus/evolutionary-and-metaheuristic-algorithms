import numpy as np
import matplotlib.pyplot as plt

from project2.greedy_local_search import greedyLocalSearch
from utils import makeDistanceMatrix, calculatePathDistance, readTspFile


def tests(function):
    data = readTspFile("../data/kroB200.tsp")
    mode = "edges"
    distanceMatrix = makeDistanceMatrix(data)
    distances = np.array(makeDistanceMatrix(data))

    paths = []
    for _ in range(1000):
        paths.append(function(distances, mode))

    distances = []
    for path in paths:
        distances.append(calculatePathDistance(path, distanceMatrix))

    minDistance = min(distances)
    minPath = paths[distances.index(minDistance)]

    print("minimalny dystans: " + str(minDistance))

    similarityToBestVertices = np.zeros(1000)
    similarityToEveryVerticesMatrix = np.zeros((1000, 1000))

    similarityToBestEdges = np.zeros(1000)
    similarityToEveryEdgesMatrix = np.zeros((1000, 1000))

    for i, path in enumerate(paths):
        for i_i, vertex in enumerate(minPath):
            if vertex in path:
                similarityToBestVertices[i] += 1

            if minPath[i_i - 1] in path and minPath[i_i] in path:
                index1 = np.where(path == minPath[i_i - 1])[0][0]
                index2 = np.where(path == minPath[i_i])[0][0]

                if path[index2 - 1] == path[index1]:
                    similarityToBestEdges[i] += 1

        similarityToBestVertices[i] = similarityToBestVertices[i]/len(path)
        similarityToBestEdges[i] = similarityToBestEdges[i]/len(path)

        for j, otherPath in enumerate(paths):
            for j_j, v in enumerate(path):
                if v in otherPath:
                    similarityToEveryVerticesMatrix[i, j] += 1

                if path[j_j - 1] in otherPath and path[j_j] in otherPath:
                    index1 = np.where(otherPath == path[j_j - 1])[0][0]
                    index2 = np.where(otherPath == path[j_j])[0][0]

                    if path[index2 - 1] == path[index1]:
                        similarityToEveryEdgesMatrix[i, j] += 1

        similarityToEveryVerticesMatrix[i] = [s/len(path) for s in similarityToEveryVerticesMatrix[i]]
        similarityToEveryEdgesMatrix[i] = [s/len(path) for s in similarityToEveryEdgesMatrix[i]]

    similarityToEveryVertices = [np.sum(s)/len(paths[0]) for s in similarityToEveryVerticesMatrix]
    similarityToEveryEdges = [np.sum(s)/len(paths[0]) for s in similarityToEveryEdgesMatrix]

    plt.scatter(distances, similarityToBestVertices)
    plt.xlabel("distances")
    plt.ylabel("similarity")
    plt.show()
    plt.clf()

    plt.scatter(distances, similarityToBestEdges)
    plt.xlabel("distances")
    plt.ylabel("similarity")
    plt.show()
    plt.clf()

    plt.scatter(distances, similarityToEveryVertices)
    plt.xlabel("distances")
    plt.ylabel("similarity")
    plt.show()
    plt.clf()

    plt.scatter(distances, similarityToEveryEdges)
    plt.xlabel("distances")
    plt.ylabel("similarity")
    plt.show()
    plt.clf()


if __name__ == '__main__':
    tests(greedyLocalSearch)
