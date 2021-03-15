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

    nx.draw_networkx_nodes(graph, dataDict)
    nx.draw_networkx_labels(graph, dataDict)
    nx.draw_networkx_edges(graph, dataDict)

    plt.show()
    plt.clf()