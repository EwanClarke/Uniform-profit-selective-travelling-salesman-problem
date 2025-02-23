import numpy as np
import random
from algorithms.utils import find_candidate_nodes, determine_best_tour


# make a copy of the adjacency matrix and fill with 1s in place of non-zero edge weights
# ant traverses graph with the edge weights and the pheromone weights contributing to the chance of the ant choosing
#   each node
# along the path the ant traversed pheromones will be placed with their values corresponding to the performance of the ant
# depending on effectiveness without, test adding negative pheromones where the ant does not complete a cycle

def stsp_ant_colony_optimisation(adjacency_matrix, max_cost, no_of_ants=250, rate_of_decay=0.7):
    pheromone_matrix = np.array([[1] * len(adjacency_matrix)] * len(adjacency_matrix))
    best_tour = []
    for i in range(no_of_ants):
        ant_tour = ant_traversal(adjacency_matrix, pheromone_matrix, max_cost)
        pheromone_matrix = update_pheromone_matrix(pheromone_matrix, ant_tour, rate_of_decay)
        best_tour = determine_best_tour(best_tour, ant_tour, adjacency_matrix)
    return best_tour


def ant_traversal(adjacency_matrix, pheromone_matrix, max_cost):
    visited_nodes = {0}
    remaining_budget = max_cost
    ant_tour = [0]

    candidate_nodes = find_candidate_nodes(adjacency_matrix, ant_tour[-1], visited_nodes, remaining_budget)
    while len(candidate_nodes) > 0:
        weights = generate_choice_weights(adjacency_matrix, pheromone_matrix, ant_tour[-1], candidate_nodes)
        next_node = random.choices(candidate_nodes, weights=weights)
        remaining_budget -= adjacency_matrix[ant_tour[-1]][next_node[0][0]]
        ant_tour.append(next_node[0][0])
        visited_nodes.add(next_node[0][0])
        candidate_nodes = find_candidate_nodes(adjacency_matrix, ant_tour[-1], visited_nodes, remaining_budget)
    ant_tour.append(0)
    return ant_tour


def generate_choice_weights(adjacency_matrix, pheromone_matrix, current_node, candidate_nodes):
    alpha = 0.6
    beta = 5
    epsilon = 1e-10
    weights = []
    traversal_costs = []
    pheromone_levels = []
    for candidate_node in candidate_nodes:
        traversal_costs.append(adjacency_matrix[current_node][candidate_node[0]]+ epsilon)
        pheromone_levels.append(pheromone_matrix[current_node][candidate_node[0]])
    for i in range(0, len(candidate_nodes)):
        weight_for_traversal = pheromone_levels[i] ** alpha / traversal_costs[i] ** beta
        weights.append(weight_for_traversal)
    return weights


def update_pheromone_matrix(pheromone_matrix, ant_tour, rate_of_decay):
    for i in range(0, len(ant_tour) - 1):
        pheromone_matrix[ant_tour[i]][ant_tour[i + 1]] += ((1 - rate_of_decay) * pheromone_matrix[i][i + 1] +
                                                          (1 - (1 / len(ant_tour))))
    return pheromone_matrix
