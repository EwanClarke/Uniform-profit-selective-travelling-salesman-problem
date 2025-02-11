from node import Node
from random import randrange
import pandas as pd
import numpy as np

def random_path(no_of_nodes:int, value_range:int):
    nodes = []
    for i in range(0, no_of_nodes):
        nodes.append(Node(i, randrange(0, value_range), randrange(0, value_range)))
    return nodes

def calculate_complete_graph_adjacency_matrix(complete_graph_nodes: [Node]):
    adjacency_matrix = pd.DataFrame(columns=[node.get_node_id() for node in complete_graph_nodes])
    for node_i in complete_graph_nodes:
        for node_j in complete_graph_nodes:
            adjacency_matrix.loc[node_j.get_node_id(), node_i.get_node_id()] = round(node_i.calculate_distance(node_j))
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