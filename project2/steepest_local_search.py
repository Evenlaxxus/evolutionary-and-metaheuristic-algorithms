import itertools
import sys

import numpy as np
import utils


def findOutsideSwap(distanceMatrix, path, not_path, i, j):
    v1 = path[i - 1]
    v2 = path[i]
    v3 = path[i + 1]
    edge1 = distanceMatrix[v1, v2]
    edge2 = distanceMatrix[v2, v3]

    newV = not_path[j]

    newEdge1 = distanceMatrix[v1, newV]
    newEdge2 = distanceMatrix[newV, v3]

    currentLength = edge1 + edge2
    newLength = newEdge1 + newEdge2

    delta = newLength - currentLength
    return (i, j), delta


def findEdgeSwap(distanceMatrix, path, i, j):
    v1 = path[i]
    v2 = path[i + 1]
    edge1 = distanceMatrix[v1, v2]

    v3 = path[j]
    v4 = path[j + 1]
    edge2 = distanceMatrix[v3, v4]

    newEdge1 = distanceMatrix[v1, v3]
    newEdge2 = distanceMatrix[v2, v4]

    currentLength = edge1 + edge2
    newLength = newEdge1 + newEdge2

    delta = newLength - currentLength
    return (i + 1, j), delta


def bestOutsideSwap(distanceMatrix, path, not_path, i):
    bestMove = tuple()
    bestDelta = sys.maxsize
    for j in range(len(not_path)):
        move, delta = findOutsideSwap(distanceMatrix, path, not_path, i, j)
        if delta < bestDelta:
            bestMove = move
            bestDelta = delta
    return bestMove, bestDelta


def bestEdgeSwap(distanceMatrix, path, i):
    bestMove = tuple()
    bestDelta = sys.maxsize
    for j in range(len(path) - 1):
        if j != i and j != i + 1 and j != i - 1:
            move, delta = findEdgeSwap(distanceMatrix, path, i, j)
            if delta < bestDelta:
                bestMove = move
                bestDelta = delta
    return bestMove, bestDelta


def getBestMove(distanceMatrix, path, not_path):
    bestMove = tuple()
    moveType = None
    bestMoveDelta = sys.maxsize
    for i in range(len(path) - 1):
        move, delta = bestOutsideSwap(distanceMatrix, path, not_path, i)
        if delta < bestMoveDelta:
            bestMove = move
            bestMoveDelta = delta
            moveType = "outside"

        move, delta = bestEdgeSwap(distanceMatrix, path, i)
        if delta < bestMoveDelta:
            bestMove = move
            bestMoveDelta = delta
            moveType = "edge"
    return moveType, bestMove, bestMoveDelta


def steepest(distanceMatrix, type):
    number_of_all = distanceMatrix.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))
    path, not_path = utils.make_random_path(number_of_half, number_of_all)

    while True:
        moveType, move, moveDelta = getBestMove(distanceMatrix, path, not_path)
        if moveDelta >= 0:
            break
        v1, v2 = move
        if moveType == "edge":
            path[v1:v2 + 1] = np.flip(path[v1:v2 + 1])
        elif moveType == "outside":
            path[v1], not_path[v2] = not_path[v2], path[v1]
    return np.append(path, path[0])


def main():
    kroA100Data = utils.readTspFile("../data/kroA100.tsp")
    utils.localSearchTester(steepest, kroA100Data, "edges")
    # utils.localSearchTester(steepest, kroA100Data, "vertices")


if __name__ == "__main__":
    main()
