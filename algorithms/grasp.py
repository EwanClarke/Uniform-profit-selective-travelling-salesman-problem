import random
from algorithms.utils import swap_edges, determine_best_tour


def stsp_grasp(adjacency_matrix, max_cost: int, alpha=0.5, alpha_rate_of_change=0.8, local_search_iterations=2):
    current_tour = [0, 0]
    current_tour_length = 0
    nodes_in_tour = {0}
    best_tour = [0, 0]
    iterations_without_improvement = 0

    while len(current_tour) < len(adjacency_matrix) + 1:
        if iterations_without_improvement == 1:
            break
        # generate all insertion deltas
        candidate_insertions = construct_list_of_candidate_insertions(adjacency_matrix, current_tour, nodes_in_tour,
                                                                      max_cost-current_tour_length)
        if len(candidate_insertions) > 0:
            sorted_candidate_insertions = sorted(candidate_insertions, key=lambda insertion: insertion[2])
            restricted_candidate_list_size = round(len(candidate_insertions) * alpha)
            if restricted_candidate_list_size < 1:
                restricted_candidate_list_size = 1
            # take the n best insertions based on the alpha value 1 for whole list or 0 for only the best
            restricted_candidate_list = sorted_candidate_insertions[:restricted_candidate_list_size]
            # randomly choose an insertion from the chosen candidate nodes
            node_to_insert = random.choice(restricted_candidate_list)
            current_tour.insert(node_to_insert[1], node_to_insert[0])
            nodes_in_tour.add(node_to_insert[0])
            current_tour_length += node_to_insert[2]

        # generate a neighbouring solution using a local search technique, 2-opt
        two_opt_tour, two_opt_tour_length = two_opt_improvement(adjacency_matrix, current_tour.copy(), current_tour_length,
                                           local_search_iterations)

        if two_opt_tour_length < current_tour_length:
            current_tour = two_opt_tour
            current_tour_length = two_opt_tour_length

        if best_tour == current_tour:
            iterations_without_improvement += 1
        else:
            iterations_without_improvement = 0
            # update the best solution
            best_tour = determine_best_tour(best_tour, current_tour, adjacency_matrix).copy()
        alpha *= alpha_rate_of_change
    return best_tour


def construct_list_of_candidate_insertions(adjacency_matrix, tour, nodes_in_tour, budget_remaining):
    candidate_insertions = []
    # loop through nodes, if not in tour find the cheapest insertion for that node
    for i in range(len(adjacency_matrix)):
        if i not in nodes_in_tour:
            cheapest_node_insertion, insertion_location = find_cheapest_insertion_for_node(adjacency_matrix, tour, i)
            # if the cheapest insertion delta is less than the remaining budget add it to the list of candidate insertions
            if cheapest_node_insertion <= budget_remaining:
                # format of candidate insertions list [(candidate_node, location, insertion_delta), (candidate_node, location, insertion_delta) ...]
                candidate_insertions.append((i, insertion_location, cheapest_node_insertion))
    return candidate_insertions


def find_cheapest_insertion_for_node(adjacency_matrix, tour, node_to_insert):
    cheapest_insertion_location = 0
    cheapest_insertion_delta = float('inf')
    insertion_location = 1
    for previous_node, next_node in zip(tour, tour[1:]):
        insertion_delta = (adjacency_matrix[previous_node][node_to_insert] + adjacency_matrix[node_to_insert][next_node]
                           - adjacency_matrix[previous_node][next_node])
        if insertion_delta < cheapest_insertion_delta:
            cheapest_insertion_delta = insertion_delta
            cheapest_insertion_location = insertion_location
        insertion_location += 1
    return cheapest_insertion_delta, cheapest_insertion_location


def two_opt_improvement(adjacency_matrix, tour, tour_length, iterations):
    total_nodes_in_path = len(tour)

    for i in range(iterations):
        improvement_found = False
        for j in range(total_nodes_in_path):
            for k in range(j + 2, total_nodes_in_path):
                length_delta = (-adjacency_matrix[tour[j]][tour[j + 1]] - adjacency_matrix[tour[k]][
                    tour[(k + 1) % total_nodes_in_path]]) + (
                                           adjacency_matrix[tour[j]][tour[k]] + adjacency_matrix[tour[j + 1]][
                                       tour[(k + 1) % total_nodes_in_path]])

                if length_delta < 0:
                    tour = swap_edges(tour, j, k)
                    tour_length += length_delta
                    improvement_found = True
        if not improvement_found:
            break
    return tour, tour_length
