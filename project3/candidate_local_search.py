import sys

import numpy as np
import utils


def findOutsideSwap(distanceMatrix, path, not_path, i, j):
    v1 = path[i - 1]
    v2 = path[i]

    if i == len(path) - 1:
        v3 = path[0]
    else:
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
    if i == len(path) - 1:
        v2 = path[0]
    else:
        v2 = path[i + 1]

    edge1 = distanceMatrix[v1, v2]

    v3 = path[j]
    if j == len(path) - 1:
        v4 = path[0]
    else:
        v4 = path[j + 1]

    edge2 = distanceMatrix[v3, v4]

    newEdge1 = distanceMatrix[v1, v3]
    newEdge2 = distanceMatrix[v2, v4]

    currentLength = edge1 + edge2
    newLength = newEdge1 + newEdge2

    delta = newLength - currentLength
    return (i + 1, j), delta


def bestOutsideSwap(distanceMatrix, path, not_path, candidates, i):
    bestMove = tuple()
    bestDelta = sys.maxsize
    for candidate in candidates:
        if candidate in not_path:
            move, delta = findOutsideSwap(distanceMatrix, path, not_path, i, np.where(not_path == candidate)[0][0])
            if delta < bestDelta:
                bestMove = move
                bestDelta = delta
    return bestMove, bestDelta


def bestEdgeSwap(distanceMatrix, path, candidates, i):
    bestMove = tuple()
    bestDelta = sys.maxsize
    for candidate in candidates:
        if candidate in path:
            move, delta = findEdgeSwap(distanceMatrix, path, i, np.where(path == candidate)[0][0])
            if delta < bestDelta:
                bestMove = move
                bestDelta = delta
    return bestMove, bestDelta


def getBestMove(distanceMatrix, path, not_path, candidatesDict):
    bestMove = tuple()
    moveType = None
    bestMoveDelta = sys.maxsize
    for i in range(len(path) - 1):
        move, delta = bestOutsideSwap(distanceMatrix, path, not_path, candidatesDict[path[i]], i)
        if delta < bestMoveDelta:
            bestMove = move
            bestMoveDelta = delta
            moveType = "outside"

        move, delta = bestEdgeSwap(distanceMatrix, path, candidatesDict[path[i]], i)
        if delta < bestMoveDelta:
            bestMove = move
            bestMoveDelta = delta
            moveType = "edge"
    return moveType, bestMove, bestMoveDelta


def getCandidates(distanceMatrix, k):
    candidatesDict = dict()
    for i in range(len(distanceMatrix)):
        candidatesDict[i] = np.argsort(distanceMatrix[i])[1:k+1]
    return candidatesDict


def steepest(distanceMatrix, starting=None):
    number_of_all = distanceMatrix.shape[0]
    number_of_half = int(np.ceil(number_of_all / 2))
    if starting is None:
        path, not_path = utils.make_random_path(number_of_half, number_of_all)
    else:
        path = starting
        not_path = np.array([p for p in range(len(distanceMatrix)) if p not in path])
    candidatesDict = getCandidates(distanceMatrix, 5)

    while True:
        moveType, move, moveDelta = getBestMove(distanceMatrix, path, not_path, candidatesDict)
        if moveDelta >= 0:
            break
        v1, v2 = move
        if moveType == "edge":
            if v1 > v2:
                toFlip = np.append(path[v1:], path[:v2 + 1])
                toFlip = np.flip(toFlip)
                v1Len = len(path[v1:])
                path[v1:] = toFlip[:v1Len]
                path[:v2 + 1] = toFlip[v1Len:]
            else:
                path[v1:v2 + 1] = np.flip(path[v1:v2 + 1])
        elif moveType == "outside":
            path[v1], not_path[v2] = not_path[v2], path[v1]
    return np.append(path, path[0])


def main():
    kroA100Data = utils.readTspFile("../data/kroB200.tsp")
    utils.localSearchTester(steepest, kroA100Data, "edges")
    # utils.localSearchTester(steepest, kroA100Data, "vertices")


if __name__ == "__main__":
    main()
