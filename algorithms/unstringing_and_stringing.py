
# unstringing stringing postoptimisation procedure from the GENIUS algorithm for the tsp (Gendreau et al., 1992)

def unstringing_algorithm(adjacency_matrix, current_tour, node_index):
    unstrung_node = current_tour[node_index]
    current_tour.pop(node_index)
    new_tour = current_tour
    return new_tour

    # for each node in the tour except for the depot node
    # remove node
    # reverse