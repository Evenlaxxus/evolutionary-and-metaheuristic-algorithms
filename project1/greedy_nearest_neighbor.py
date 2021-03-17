import random
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import distance_matrix


if __name__ == "__main__":
    coordinates = []
    cities = []
    lines = {}
    file = open("data/kroA100.tsp", "r")
    content = file.readlines()
    for line in content[6:106]:
        numbers = line.split()
        cities.append(numbers[0])
        coordinates.append([float(numbers[1]), float(numbers[2])])
        lines[numbers[0]] = {}
        lines[numbers[0]]["x"] = float(numbers[1])
        lines[numbers[0]]["y"] = float(numbers[2])
    print(len(cities))
    number_of_cities = None
    if len(cities) % 2 == 0:
        number_of_cities = len(cities)/2
    else:
        number_of_cities = len(cities)/2 + 1
    df = pd.DataFrame(coordinates, columns=['xcord', 'ycord'], index=cities)
    matrix = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
    matrix = matrix.round(0)
    #print(matrix)
    whole_matrix = matrix
    unvisited = set(cities)
    start_1 = random.choice(tuple(cities))
    tour_1 = [start_1]
    unvisited = unvisited - {start_1}
    matrix = matrix.drop(index=start_1)
    '''start_2 = random.choice(tuple(cities))
    tour_2 = [start_2]
    unvisited = unvisited - {start_2}
    matrix = matrix.drop(index=start_2)'''
    print(matrix)
    print(unvisited)
    tour_1_length = 0
    #tour_2_length = 0
    added_cities = 1
    print(number_of_cities)
    while added_cities < number_of_cities:
       last_element_1 = tour_1[-1]
       #print(last_element_1)
       #last_element_2 = tour_2[-1]
       #print(last_element_2)
       id_min_value_1 = matrix[last_element_1].idxmin()
       tour_1_length += matrix[last_element_1][id_min_value_1]
       #print("id " + id_min_value_1)
       #print(matrix[last_element_1])
       tour_1.append(id_min_value_1)
       #print(tour_1)
       unvisited.remove(id_min_value_1)
       #print(len(unvisited))
       #print("last" + last_element_1)
       matrix = matrix.drop(index=id_min_value_1)
       '''id_min_value_2 = matrix[last_element_2].idxmin()
       tour_2_length += matrix[last_element_2][id_min_value_2]'''
       #print(id_min_value_1)
       #print(id_min_value_2)
       '''tour_2.append(id_min_value_2)
       unvisited.remove(id_min_value_2)
       matrix = matrix.drop(index=id_min_value_2)'''
       added_cities += 1
    tour_1_length += whole_matrix[tour_1[0]][tour_1[-1]]
    #tour_2_length += whole_matrix[tour_2[0]][tour_2[-1]]

    print("t1= ", tour_1)
    print(tour_1_length, len(tour_1))
    print(lines)
    tour_1.append(tour_1[0])
    plot_x = []
    plot_y = []
    for city in tour_1:
        plot_x.append(lines[city]['x'])
        plot_y.append(lines[city]['y'])
    print(plot_x)
    print(plot_y)
    plt.plot(plot_x, plot_y, '-o')
    plt.show()
    '''print("t1= ", tour_2)
    print(tour_2_length)'''
