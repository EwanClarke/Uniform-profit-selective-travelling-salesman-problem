from node import Node
from random import randrange
import networkx as nx
from matplotlib import pyplot as plt
from path_utilities import *
import pandas as pd
from nearest_neighbour_adaption import stsp_nearest_neighbour
from cheapest_insertion import stsp_cheapest_insertion
import tsplib95

def calculate_complete_graph_adjacency_matrix(complete_graph_nodes: [Node]):
    adjacency_matrix = pd.DataFrame(columns=[node.get_node_id() for node in complete_graph_nodes])
    for node_i in complete_graph_nodes:
        for node_j in complete_graph_nodes:
            adjacency_matrix.loc[node_j.get_node_id(), node_i.get_node_id()] = node_i.calculate_distance(node_j)
    adjacency_matrix.index = [node.get_node_id() for node in complete_graph_nodes]
    return adjacency_matrix


def display_path(path, value_range:int, nodes_not_on_path=None):
    if nodes_not_on_path is None:
        nodes_not_on_path = []

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.xlim(-100, value_range+100)
    plt.ylim(-100, value_range+100)
    plt.rcParams["figure.autolayout"] = False

    x_coordinates = []
    y_coordinates = []

    for i in range(0, len(path)):
        x_coordinates.append(path[i].x)
        y_coordinates.append(path[i].y)
        if i < len(path)-1:
            plt.plot([path[i].x, path[i+1].x], [path[i].y, path[i+1].y])
        else:
            plt.plot([path[i].x, path[0].x], [path[i].y, path[0].y])
    for node in nodes_not_on_path:
        x_coordinates.append(node.x)
        y_coordinates.append(node.y)
    plt.scatter(x_coordinates[1:], y_coordinates[1:])
    plt.scatter(x_coordinates[0], y_coordinates[0], marker="*", edgecolors='r', s=80)

def display_path_indexes(all_nodes, path_indexes, value_range):
    path = []
    for index in path_indexes:
        path.append(all_nodes[index])

    nodes_not_on_path = []
    for i in range(0, len(all_nodes)):
        if i not in path_indexes:
            nodes_not_on_path.append(all_nodes[i])

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.xlim(-100, value_range+100)
    plt.ylim(-100, value_range+100)
    plt.rcParams["figure.autolayout"] = False

    x_coordinates = []
    y_coordinates = []

    for i in range(0, len(path)):
        x_coordinates.append(path[i].x)
        y_coordinates.append(path[i].y)
        if i < len(path)-1:
            plt.plot([path[i].x, path[i+1].x], [path[i].y, path[i+1].y])
        else:
            plt.plot([path[i].x, path[0].x], [path[i].y, path[0].y])
    for node in nodes_not_on_path:
        x_coordinates.append(node.x)
        y_coordinates.append(node.y)
    plt.scatter(x_coordinates[1:], y_coordinates[1:])
    plt.scatter(x_coordinates[0], y_coordinates[0], marker="*", edgecolors='r', s=80)



if __name__ == '__main__':
    value_range:int = 10000
    max_cost = 15000
    no_of_nodes = 10

    path = random_path(no_of_nodes, value_range)

    adjacency_matrix = calculate_complete_graph_adjacency_matrix(path)
    adjacency_matrix = adjacency_matrix.to_numpy()


    # fig = plt.figure()
    #
    # ax1 = plt.subplot(1, 2, 1)
    # display_path([], value_range, path)
    # plt.xticks([])
    # plt.yticks([])
    # ax1.set_aspect('equal', adjustable='box')
    # ax1.set_aspect(1. / ax1.get_data_ratio())
    # #current_length = path_length(tour)
    # #print(f"tour length = {current_length}")
    #
    path_indexes = stsp_nearest_neighbour(adjacency_matrix, max_cost)
    path_indexes = stsp_cheapest_insertion(adjacency_matrix, max_cost)

    # ax2 = plt.subplot(1, 2, 2)
    # display_path_indexes(path, path_indexes, value_range)
    # plt.xticks([])
    # plt.yticks([])
    # ax2.set_aspect('equal', adjustable='box')
    # ax2.set_aspect(1. / ax2.get_data_ratio())
    # #current_length = path_length(tour)
    # #print_path("test tour after", tour)
    # #print(f"tour length = {current_length}")
    # plt.show()

    # print(adjacency_matrix)
    # A = np.matrix(adjacency_matrix)
    # G = nx.DiGraph()
    # G.add_weighted_edges_from(adjacency_matrix)
    # plt.show()

    for i, row in enumerate(adjacency_matrix):
        for j in range(0, len(row)):
            adjacency_matrix[i][j] = round(adjacency_matrix[i][j], 2)

    G = nx.from_numpy_array(np.array(adjacency_matrix).astype(float), create_using=nx.DiGraph)

    weight = nx.get_edge_attributes(G, 'weight')
    print(weight)
    new_weights = {}
    for i in range(0, len(path_indexes)-1):
        current_node = path_indexes[i]
        next_node = path_indexes[i+1]
        new_weights[(current_node,next_node)] = weight[(current_node,next_node)]
    print(new_weights)


    new_G = nx.DiGraph() # generate adjacency matrix for the new graph representing the solution
    nx.set_edge_attributes(new_G, new_weights)

    pos = nx.spring_layout(G)
    nx.draw(new_G, pos=pos, with_labels=True, node_size = 300, node_color = 'r')
    nx.draw_networkx_edge_labels(new_G, pos=pos, edge_labels=new_weights, font_size=10)
    plt.show()
    # draw the nodes and edges separately so that nodes not in the graph are also displayed





