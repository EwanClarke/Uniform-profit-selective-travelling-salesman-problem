from node import Node
from random import randrange
import numpy as np
import pandas as pd

def random_path(no_of_nodes:int, value_range:int):
    nodes = []
    for i in range(0, no_of_nodes):
        nodes.append(Node(i, randrange(0, value_range), randrange(0, value_range)))
    return nodes

def calculate_complete_graph_adjacency_matrix(complete_graph_nodes: [Node]):
    adjacency_matrix = pd.DataFrame(columns=[node.get_node_id() for node in complete_graph_nodes])
    for node_i in complete_graph_nodes:
        for node_j in complete_graph_nodes:
            adjacency_matrix.loc[node_j.get_node_id(), node_i.get_node_id()] = node_i.calculate_distance(node_j)
    adjacency_matrix.index = [node.get_node_id() for node in complete_graph_nodes]
    return adjacency_matrix

def generate_random_symmetric_complete_graph_adjacency_matrix(no_of_nodes, max_distance, min_distance = 1):
    adjacency_matrix = np.array([[0]*no_of_nodes]*no_of_nodes)
    for i in range(no_of_nodes):
        for j in range(no_of_nodes):
            if i == j:
                continue
            edge_weight = randrange(min_distance, max_distance)
            adjacency_matrix[i][j] = edge_weight
            adjacency_matrix[j][i] = edge_weight
    return adjacency_matrix


def path_length(path):
    if len(path) <= 1:
        return 0
    nodes = len(path)
    length = path[-1].calculate_distance(path[0])
    for i in range(0, nodes-1):
        length += path[i].calculate_distance(path[i+1])
    return length

def tour_length_adjacency_matrix(adjacency_matrix, tour):
    total_length = 0
    current_node = tour[0]
    for next_node in tour[1:]:
        total_length += adjacency_matrix[current_node][next_node]
        current_node = next_node
    total_length += adjacency_matrix[tour[0]][tour[-1]]
    return total_length


def print_path(path_name, path):
    print(f"{path_name} = [", end="")
    for i in range(0, len(path)):
        if i % 10 == 0:
            print("")

        if i < len(path)-1:
            print(f"[{path[i].x}, {path[i].y}], ", end="")
        else:
            print(f"[{path[i].x}, {path[i].y}]\n]")

def swap_edges(path, i, j):
    i += 1
    while i < j:
        temp = path[i]
        path[i] = path[j]
        path[j] = temp
        i += 1
        j -= 1


