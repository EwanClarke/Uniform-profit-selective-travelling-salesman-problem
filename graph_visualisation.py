import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

def plot_from_nodes(path, value_range:int, nodes_not_on_path=None):
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

def plot_from_path_indexes(all_nodes, path_indexes, value_range):
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

def display_matplotlib_comparison(path, path_indexes, value_range):
    fig = plt.figure()
    ax1 = plt.subplot(1, 2, 1)
    plot_from_nodes([], value_range, path)
    plt.xticks([])
    plt.yticks([])
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_aspect(1. / ax1.get_data_ratio())

    ax2 = plt.subplot(1, 2, 2)
    plot_from_path_indexes(path, path_indexes, value_range)
    plt.xticks([])
    plt.yticks([])
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_aspect(1. / ax2.get_data_ratio())
    plt.show()

def display_networkx(adjacency_matrix, no_of_nodes, path_indexes):
    for i, row in enumerate(adjacency_matrix):
        for j in range(0, len(row)):
            adjacency_matrix[i][j] = round(adjacency_matrix[i][j], 2)

    G = nx.from_numpy_array(np.array(adjacency_matrix).astype(float), create_using=nx.DiGraph)

    weight = nx.get_edge_attributes(G, 'weight')
    solution_weights = {}
    for i in range(0, len(path_indexes)-1):
        current_node = path_indexes[i]
        next_node = path_indexes[i+1]
        solution_weights[(current_node, next_node)] = weight[(current_node, next_node)]

    solution_adjacency_matrix = np.array([[0]*no_of_nodes]*no_of_nodes)
    for current_node, next_node in zip(path_indexes, path_indexes[1:]):
        solution_adjacency_matrix[current_node][next_node] = adjacency_matrix[current_node][next_node]

    solution_G = nx.from_numpy_array(solution_adjacency_matrix.astype(float), create_using=nx.DiGraph)
    pos = nx.spring_layout(G)
    nx.draw(solution_G, pos=pos, with_labels=True, node_size = 300, node_color = 'r')
    nx.draw_networkx_edge_labels(solution_G, pos=pos, edge_labels=solution_weights, font_size=10)
    plt.show()

def display_networkx_positional(adjacency_matrix, no_of_nodes, path_indexes, pos):
    for i, row in enumerate(adjacency_matrix):
        for j in range(0, len(row)):
            adjacency_matrix[i][j] = round(adjacency_matrix[i][j], 2)

    G = nx.from_numpy_array(np.array(adjacency_matrix).astype(float), create_using=nx.DiGraph)

    weight = nx.get_edge_attributes(G, 'weight')
    solution_weights = {}
    for i in range(0, len(path_indexes)-1):
        current_node = path_indexes[i]
        next_node = path_indexes[i+1]
        solution_weights[(current_node, next_node)] = weight[(current_node, next_node)]

    solution_adjacency_matrix = np.array([[0]*no_of_nodes]*no_of_nodes)
    for current_node, next_node in zip(path_indexes, path_indexes[1:]):
        solution_adjacency_matrix[current_node][next_node] = adjacency_matrix[current_node][next_node]

    solution_G = nx.from_numpy_array(solution_adjacency_matrix.astype(float), create_using=nx.DiGraph)
    nx.draw(solution_G, pos=pos, with_labels=True, node_size = 300, node_color = 'r', font_size=6)
    nx.draw_networkx_edge_labels(solution_G, pos=pos, edge_labels=solution_weights, font_size=6)
    plt.show()