from algorithms.cheapest_insertion import stsp_cheapest_insertion
from algorithms.nearest_neighbour_adaption import stsp_nearest_neighbour
from utils import determine_best_tour, tour_length_adjacency_matrix


def stsp_exact_algorithm(adjacency_matrix, max_cost):
    h1_result = stsp_nearest_neighbour(adjacency_matrix, max_cost)
    h2_result = stsp_cheapest_insertion(adjacency_matrix, max_cost)
    best_result = determine_best_tour(h1_result, h2_result, adjacency_matrix)
    # calculate upper bound
    node_weights = calculate_node_weights(adjacency_matrix, max_cost)
    upper_bound = solve_uniform_profit_knapsack(node_weights, max_cost)
    # compare the best heuristic result to the upper bound, terminate if they are the same
    if upper_bound == len(best_result):
        return best_result
    # calculate the sum of the first n node weights
    sums_of_lowest_node_weights = []
    node_weights_sorted = sorted(node_weights)
    for i in range(0, upper_bound):
        sums_of_lowest_node_weights.append(sum(node_weights_sorted[0:i]))

    # branching process - partitioning schemes
    result = branch_and_bound([0, 0], adjacency_matrix, max_cost, max_cost, [0, 0],
                              sums_of_lowest_node_weights, upper_bound)
    return result


def calculate_node_weights(adjacency_matrix, max_cost, alpha=0.5):
    # calculate node weights using wj=a min{cij}+(1-a)min{Cjk}, j=1,...,n
    node_weights = []
    for i in range(0, len(adjacency_matrix)):
        minimum_weight_from_other = float('inf')
        minimum_weight_to_other = float('inf')
        for j in range(0, len(adjacency_matrix[i])):
            if i == j:
                continue
            if adjacency_matrix[i][j] < minimum_weight_from_other:
                minimum_weight_from_other = adjacency_matrix[i][j]
            if adjacency_matrix[j][i] < minimum_weight_to_other:
                minimum_weight_to_other = adjacency_matrix[j][i]
        node_weights.append(alpha * minimum_weight_from_other + (1 - alpha) * minimum_weight_to_other)
    return node_weights


def solve_uniform_profit_knapsack(item_weights, capacity, required_items=None):
    items_in_knapsack = 0
    knapsack_weight = 0
    if required_items is None:
        required_items = [0]
    else:
        required_items = sorted(required_items, reverse=True)

    for item_index in required_items:
        knapsack_weight += item_weights[item_index]
        item_weights.pop(item_index)

    item_weights_sorted = sorted(item_weights)  # O(n log n)
    if len(item_weights_sorted) == 0:
        return items_in_knapsack
    while knapsack_weight + item_weights_sorted[0] < capacity:
        knapsack_weight += item_weights_sorted[0]
        item_weights_sorted.pop(0)
        items_in_knapsack += 1
    return items_in_knapsack


def branch_and_bound(current_solution: list, adjacency_matrix, budget_remaining, budget, best_solution,
                     node_weight_sums, upper_bound, candidate_nodes=None):
    candidate_nodes = calculate_candidate_nodes(current_solution, budget_remaining, adjacency_matrix, candidate_nodes)
    if len(current_solution) < len(best_solution) and budget_remaining < node_weight_sums[
        len(best_solution) - len(current_solution)]:
        return best_solution
    if len(candidate_nodes) == 0:
        if ((len(current_solution) > len(best_solution)) or
                (len(current_solution) == len(best_solution) and
                 budget_remaining > budget - tour_length_adjacency_matrix(adjacency_matrix, best_solution))):
            return current_solution

        return best_solution

    for candidate in candidate_nodes:
        branch_budget_remaining = budget_remaining - calculate_insertion_delta(adjacency_matrix, current_solution,
                                                                               candidate)
        branch_tour = current_solution[0:-1] + [candidate] + [current_solution[-1]]
        branch_candidate_nodes = [node for node in candidate_nodes if node != candidate]
        best_solution = branch_and_bound(branch_tour, adjacency_matrix, branch_budget_remaining, budget, best_solution,
                                         node_weight_sums, upper_bound, branch_candidate_nodes)
    return best_solution


def calculate_candidate_nodes(current_solution, budget_remaining, adjacency_matrix, candidate_nodes):
    if candidate_nodes is None:
        candidate_nodes = range(1, len(adjacency_matrix))

    new_candidate_nodes = []
    for candidate in candidate_nodes:
        insertion_delta = calculate_insertion_delta(adjacency_matrix, current_solution, candidate)
        if insertion_delta <= budget_remaining:
            new_candidate_nodes.append(candidate)

    return new_candidate_nodes


def calculate_insertion_delta(adjacency_matrix, current_solution, node_to_insert):
    return (adjacency_matrix[current_solution[-2]][node_to_insert] +
            adjacency_matrix[node_to_insert][current_solution[-1]] -
            adjacency_matrix[current_solution[-2]][current_solution[-1]])
