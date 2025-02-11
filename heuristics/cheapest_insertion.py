import numpy as np
from heuristics.utils import runtime_counter
    # step 1
    # find node to insert with minimal ratio (d0j + dj0)/h
    # step 2
    # if the tour contains all nodes in the set of nodes stop
    # find node not in the tour and two nodes which minimise the ratio (dij + djk - dik)/pj and
    # tour length + dij + djk - dik <= max cost
    # repeat until no more exist which meet the requirement

    # O(n^2 log n)
def stsp_cheapest_insertion(adjacency_matrix: np.array([[int]]), max_cost: int):
    previous_node = 0
    next_node = 0
    current_tour = np.array([0,0])
    nodes_in_tour: {int} = {0}
    tour_length = 0

    while len(current_tour) < len(adjacency_matrix)+1:
        cheapest_insertion_for_each_position = []
        cheapest_insertion_node_for_each_position = []
        for previous_node, next_node in zip(current_tour, current_tour[1:]):
            insertion_deltas = construct_list_of_insertion_deltas(adjacency_matrix, previous_node, next_node)
            cheapest_insertion = find_cheapest_candidate_insertion_delta(insertion_deltas, nodes_in_tour)
            cheapest_insertion_node = find_cheapest_candidate_insertion_node(insertion_deltas, cheapest_insertion,
                                                                             nodes_in_tour)
            cheapest_insertion_for_each_position.append(cheapest_insertion)
            cheapest_insertion_node_for_each_position.append(cheapest_insertion_node)
        cheapest_insertion_index = cheapest_insertion_for_each_position.index(min(cheapest_insertion_for_each_position))
        if cheapest_insertion_for_each_position[cheapest_insertion_index] + tour_length <= max_cost:
            current_tour = np.insert(current_tour, cheapest_insertion_index+1, cheapest_insertion_node_for_each_position[cheapest_insertion_index])
            nodes_in_tour.add(cheapest_insertion_node_for_each_position[cheapest_insertion_index])
            tour_length += cheapest_insertion_for_each_position[cheapest_insertion_index]
        else:
            break
    return current_tour


def construct_list_of_insertion_deltas(adjacency_matrix, previous_node, next_node):
    distances_from_previous = adjacency_matrix[previous_node].reshape(len(adjacency_matrix[previous_node]), 1)
    distances_to_next = adjacency_matrix[:, [next_node]]
    all_insertion_costs_separate = np.hstack((distances_from_previous, distances_to_next))
    all_insertion_deltas = [sum(distances) - adjacency_matrix[previous_node][next_node] for distances in
                            all_insertion_costs_separate]
    return all_insertion_deltas

def find_cheapest_candidate_insertion_delta(insertion_deltas, nodes_in_tour):
    candidate_node_insertion_deltas = np.delete(insertion_deltas, list(nodes_in_tour))
    cheapest_insertion_delta = np.min(candidate_node_insertion_deltas)
    return cheapest_insertion_delta

def find_cheapest_candidate_insertion_node(insertion_deltas, cheapest_insertion_delta, nodes_in_tour):
    cheapest_nodes_to_insert = list(np.where(np.array(insertion_deltas) == cheapest_insertion_delta)[0])
    node_to_insert = [node for node in cheapest_nodes_to_insert if node not in nodes_in_tour][0]
    return node_to_insert

    # step 3
    # apply US procedure (GENIUS) from to the tour to find a shorter tour
    # unstringing - consider both implementations for k-neighbours as defined by neighbourhood size
    # if a shorter tour is not found stop, otherwise go back to step 2
