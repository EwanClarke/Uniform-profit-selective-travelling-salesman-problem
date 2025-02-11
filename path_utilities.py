
def tour_length_adjacency_matrix(adjacency_matrix, tour):
    total_length = 0
    current_node = tour[0]
    for next_node in tour[1:]:
        total_length += adjacency_matrix[current_node][next_node]
        current_node = next_node
    total_length += adjacency_matrix[tour[0]][tour[-1]]
    return total_length


def print_path(path_name, path):
    print(f"{path_name} = [", end="")
    for i in range(0, len(path)):
        if i % 10 == 0:
            print("")

        if i < len(path)-1:
            print(f"[{path[i].x}, {path[i].y}], ", end="")
        else:
            print(f"[{path[i].x}, {path[i].y}]\n]")

