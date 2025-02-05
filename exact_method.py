from heuristics.cheapest_insertion import stsp_cheapest_insertion
from heuristics.nearest_neighbour_adaption import stsp_nearest_neighbour


# exact algorithm as outlined by Laporte & Martello (1988)

def stsp_exact_algorithm(adjacency_matrix, max_cost):
    h1_result = stsp_nearest_neighbour(adjacency_matrix, max_cost)
    h2_result = stsp_cheapest_insertion(adjacency_matrix, max_cost)
    # calculate upper bound

    # function to evaluate the methods
    evaluate_results(h1_result, h2_result, adjacency_matrix, max_cost)

def calculate_upper_bound(adjacency_matrix, max_cost):

    pass
    # exact continuous knapsack problem algorithm



def evaluate_results(first_result, second_result, adjacency_matrix, max_cost):
    pass

