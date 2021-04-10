import random
import pandas as pd
from scipy.spatial import distance_matrix
import utils


def greedy_nearest_neighbor():
    coordinates = []
    cities = []
    lines_name_x_y = {}
    file = open("../data/kroA100.tsp", "r")
    content = file.readlines()
    for line in content[6:106]:
        numbers = line.split()
        cities.append(numbers[0])
        coordinates.append([float(numbers[1]), float(numbers[2])])
        lines_name_x_y[numbers[0]] = {}
        lines_name_x_y[numbers[0]]["x"] = float(numbers[1])
        lines_name_x_y[numbers[0]]["y"] = float(numbers[2])
    if len(cities) % 2 == 0:
        number_of_cities = len(cities) / 2
    else:
        number_of_cities = len(cities) / 2 + 1
    df = pd.DataFrame(coordinates, columns=['xcord', 'ycord'], index=cities)
    matrix = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
    matrix = matrix.round(0)
    whole_matrix = matrix
    unvisited = set(cities)
    start_1 = random.choice(tuple(cities))
    tour_1 = [start_1]
    unvisited = unvisited - {start_1}
    matrix = matrix.drop(index=start_1)
    tour_1_length = 0
    added_cities = 1
    while added_cities < number_of_cities:
        last_element_1 = tour_1[-1]
        id_min_value_1 = matrix[last_element_1].idxmin()
        tour_1_length += matrix[last_element_1][id_min_value_1]
        tour_1.append(id_min_value_1)
        unvisited.remove(id_min_value_1)
        matrix = matrix.drop(index=id_min_value_1)
        added_cities += 1
    tour_1_length += whole_matrix[tour_1[0]][tour_1[-1]]
    tour_1.append(tour_1[0])
    return tour_1


if __name__ == "__main__":
    kroA100Data = utils.readTspFile("../data/kroA100.tsp")
    kroA100 = greedy_nearest_neighbor()
    kroA100 = [int(i)-1 for i in kroA100]
    print(kroA100)
    utils.drawGraph(kroA100Data, kroA100)