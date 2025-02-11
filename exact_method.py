from heuristics.cheapest_insertion import stsp_cheapest_insertion
from heuristics.nearest_neighbour_adaption import stsp_nearest_neighbour
from path_utilities import tour_length_adjacency_matrix

# exact algorithm as outlined by Laporte & Martello (1988)

def stsp_exact_algorithm(adjacency_matrix, max_cost):
    h1_result = stsp_nearest_neighbour(adjacency_matrix, max_cost)
    h2_result = stsp_cheapest_insertion(adjacency_matrix, max_cost)
    best_result = determine_best_tour(h1_result, h2_result, adjacency_matrix)

    upper_bound = calculate_upper_bound_1(adjacency_matrix, max_cost)
    print(upper_bound)
    # compare the best heuristic result to the upper bound, terminate if they are the same
    if upper_bound == tour_length_adjacency_matrix(adjacency_matrix, best_result):
        return best_result
    # branching process - partitioning schemes



def determine_best_tour(first_tour, second_tour, adjacency_matrix):
    best_tour = first_tour if len(first_tour) > len(second_tour) else second_tour
    if len(first_tour) == len(second_tour):
        first_tour_length = tour_length_adjacency_matrix(adjacency_matrix, first_tour)
        second_tour_length = tour_length_adjacency_matrix(adjacency_matrix, second_tour)
        best_tour = first_tour if first_tour_length < second_tour_length else second_tour
    return best_tour

def calculate_upper_bound_1(adjacency_matrix, max_cost, alpha = 0.5):
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
        node_weights.append(alpha*minimum_weight_from_other + (1-alpha)*minimum_weight_to_other)
    # solve the knapsack problem, or find its upper bound
    knapsack_solution = solve_uniform_profit_knapsack(node_weights, max_cost)
    # the knapsack problem upper bound will not be less than the optimal solution of the problem
    return knapsack_solution

def calculate_upper_bound_2(adjacency_matrix, max_cost, alpha = 0.5):
    pass
    # for every combination of 2 nodes, neither being node 1
    # find pairs r, s which satisfy c1s + csr + cr1 <= c
    # find

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

    item_weights_sorted = sorted(item_weights) # O(n log n)
    while knapsack_weight + item_weights_sorted[0] < capacity:
        knapsack_weight += item_weights_sorted[0]
        item_weights_sorted.pop(0)
        items_in_knapsack += 1
    return items_in_knapsack

def calculate_lower_bound(adjacency_matrix, max_cost):
    pass

def dominates():
    pass

def first_partitioning_scheme(current_path, adjacency_matrix, max_cost):
    pass
    # generate a descendant node for each vertex which can be included in the tour which does not produce a dominated solution
    # a vertex ui dominates another uj if

def second_partitioning_scheme():
    pass
