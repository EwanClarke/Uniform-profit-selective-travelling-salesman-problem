from path_utilities import *
from heapq import heapify, heappush, heappop
from edge_improvement import EdgeImprovement

# TODO: reimplement 2-opt to use adjacency matrix instead of node objects and edge improvement objects

def two_opt(path):
    total_nodes = len(path)
    found_improvement = True
    current_length = path_length(path)

    while found_improvement:
        found_improvement = False
        for i in range(0, total_nodes-1):
            for j in range(i+2, total_nodes):
                length_delta = (-path[i].calculate_distance(path[i+1]) - path[j].calculate_distance(path[(j+1)%total_nodes]) +
                                path[i].calculate_distance(path[j]) + path[i+1].calculate_distance(path[(j+1)%total_nodes]))

                if length_delta < 0:
                    swap_edges(path, i, j)
                    current_length += length_delta
                    found_improvement = True


def modified_two_opt(path, max_cost: int):
    total_nodes = len(path)
    found_improvement = True
    current_length = path_length(path)

    while found_improvement:
        found_improvement = False
        for i in range(0, total_nodes - 1):
            for j in range(i + 2, total_nodes):
                length_delta = (-path[i].calculate_distance(path[i + 1]) - path[j].calculate_distance(
                    path[(j + 1) % total_nodes]) +
                                path[i].calculate_distance(path[j]) + path[i + 1].calculate_distance(
                            path[(j + 1) % total_nodes]))

                if length_delta < 0:
                    swap_edges(path, i, j)
                    current_length += length_delta
                    found_improvement = True

    removed_edge_improvements = []
    heapify(removed_edge_improvements)
    for i in range(0, len(path)):
        next_index = i + 1
        index_after_next = i + 2
        if i == len(path) - 2:
            index_after_next = 0
        elif i == len(path) - 1:
            next_index = 0
            index_after_next = 1

        length_delta = (-path[i].calculate_distance(path[next_index]) - path[next_index].calculate_distance(path[index_after_next]) +
                        path[i].calculate_distance(path[index_after_next]))

        if length_delta < 0:
            heappush(removed_edge_improvements, EdgeImprovement(path[i].id, length_delta))

    removed_nodes = []
    while current_length > max_cost:
        if len(path) == 3:
            for node in path:
                removed_nodes.append(node)
            path = path.clear()
            return removed_nodes
        edge_improvement = heappop(removed_edge_improvements)
        index = 0
        for i in range(0, len(path)):
            if edge_improvement.node_id == path[i].id:
                index = i
                break

        index_to_remove = index + 1
        if index == len(path) - 1:
            index_to_remove = 0
        removed_nodes.append(path[index_to_remove])
        path.pop(index_to_remove)
        current_length += edge_improvement.improvement

        if index > len(path) - 2:
            index -= 1
        next_index = index + 1
        index_after_next = index + 2
        if index == len(path) - 2:
            index_after_next = 0
        elif index == len(path)-1:
            next_index = 0
            index_after_next = 1

        length_delta = (-path[index].calculate_distance(path[next_index]) - path[next_index].calculate_distance(path[index_after_next]) +
                        path[index].calculate_distance(path[index_after_next]))

        heappush(removed_edge_improvements, EdgeImprovement(edge_improvement.node_id, length_delta))

    total_nodes = len(path)
    found_improvement = True
    current_length = path_length(path)

    while found_improvement:
        found_improvement = False
        for i in range(0, total_nodes - 1):
            for j in range(i + 2, total_nodes):
                length_delta = (-path[i].calculate_distance(path[i + 1]) - path[j].calculate_distance(
                    path[(j + 1) % total_nodes]) +
                                path[i].calculate_distance(path[j]) + path[i + 1].calculate_distance(
                            path[(j + 1) % total_nodes]))

                if length_delta < 0:
                    swap_edges(path, i, j)
                    current_length += length_delta
                    found_improvement = True
    return removed_nodes


