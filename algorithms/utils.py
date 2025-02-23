from time import perf_counter


def swap_edges(path, i, j):
    i += 1
    while i < j:
        temp = path[i]
        path[i] = path[j]
        path[j] = temp
        i += 1
        j -= 1
    return path


def path_length(path):
    if len(path) <= 1:
        return 0
    nodes = len(path)
    length = path[-1].calculate_distance(path[0])
    for i in range(0, nodes - 1):
        length += path[i].calculate_distance(path[i + 1])
    return length


def find_candidate_nodes(adjacency_matrix, current_node, visited_nodes, remaining_budget):
    candidate_nodes = []
    for i, distance in enumerate(adjacency_matrix[current_node]):
        if i not in visited_nodes and distance + adjacency_matrix[i][0] < remaining_budget:  # distance to depot node not considered in original formulation
            candidate_nodes.append((i, distance))
    if len(candidate_nodes) > 0:
        return sorted(candidate_nodes, key=lambda node: node[1])
    return []


def determine_best_tour(first_tour, second_tour, adjacency_matrix):
    best_tour = first_tour if len(first_tour) > len(second_tour) else second_tour
    if len(first_tour) == len(second_tour):
        first_tour_length = tour_length_adjacency_matrix(adjacency_matrix, first_tour)
        second_tour_length = tour_length_adjacency_matrix(adjacency_matrix, second_tour)
        best_tour = first_tour if first_tour_length < second_tour_length else second_tour
    return best_tour


def tour_length_adjacency_matrix(adjacency_matrix, tour):
    total_length = 0
    current_node = tour[0]
    for next_node in tour[1:]:
        total_length += adjacency_matrix[current_node][next_node]
        current_node = next_node
    total_length += adjacency_matrix[tour[0]][tour[-1]]
    return total_length
