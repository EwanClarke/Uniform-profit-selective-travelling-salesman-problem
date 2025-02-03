import numpy as np
from path_utilities import *

def nearest_neighbour(path):
    visited_nodes = []
    for i, node in enumerate(path):
        visited_nodes.append(node)
        nearest_node_distance = float('inf')
        nearest_node_index = i
        for j, comparison_node in enumerate(path[:-1]):
            distance_between_nodes = node.calculate_distance(comparison_node)
            if comparison_node in visited_nodes:
                continue

            if distance_between_nodes < nearest_node_distance:
                nearest_node_distance = distance_between_nodes
                nearest_node_index = j
        swap_edges(path, i, nearest_node_index)
    return path

# O(n^2)
def stsp_nearest_neighbour(adjacency_matrix, max_cost):
    distance_remaining = max_cost
    current_node = 0
    visited_nodes = []
    path = []
    path.append(0)
    visited_nodes.append(0)
    candidate_nodes = find_candidate_nodes(adjacency_matrix, current_node, visited_nodes, distance_remaining)
    while len(candidate_nodes) > 0:
        current_node = candidate_nodes[0][0]
        path.append(current_node)
        visited_nodes.append(current_node)
        distance_remaining -= candidate_nodes[0][1]
        candidate_nodes = find_candidate_nodes(adjacency_matrix, current_node, visited_nodes, distance_remaining)
    return path.append(0)

def find_candidate_nodes(adjacency_matrix, current_node, visited_nodes, distance_remaining):
    candidate_nodes = []
    for i, distance in enumerate(adjacency_matrix[current_node]):
        if i not in visited_nodes and distance < distance_remaining:
            candidate_nodes.append((i,distance))
    if len(candidate_nodes) > 0:
        return sorted(candidate_nodes, key=lambda node: node[1])
    return []



