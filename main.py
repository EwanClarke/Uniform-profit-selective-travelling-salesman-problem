from heuristics.cheapest_insertion import stsp_cheapest_insertion
from heuristics.nearest_neighbour_adaption import stsp_nearest_neighbour
from visualise_path import display_networkx_positional, display_matplotlib_comparison
import tsplib95
import networkx as nx
from matplotlib import pyplot as plt
from path_utilities import tour_length_adjacency_matrix

if __name__ == '__main__':
    value_range:int = 400
    max_cost = 1000
    no_of_nodes = 10
    problem = tsplib95.load("problems/tsp225.tsp")

    if problem.is_depictable():
        pass

    pos = dict(zip(range(0, len(list(problem.get_nodes()))), list(problem.node_coords.values())))
    G = problem.get_graph()
    # nx.draw(G, problem.node_coords)
    # plt.show()
    adjacency_matrix = nx.to_numpy_array(G)



    path_indexes = stsp_cheapest_insertion(adjacency_matrix, max_cost)
    #path_indexes = stsp_nearest_neighbour(adjacency_matrix, max_cost)
    print(tour_length_adjacency_matrix(adjacency_matrix, path_indexes))
    print(path_indexes)
    display_networkx_positional(adjacency_matrix, len(adjacency_matrix), path_indexes, pos)

    # nodes = random_path(no_of_nodes, value_range)
    # adjacency_matrix = calculate_complete_graph_adjacency_matrix(nodes).to_numpy()
    # adjacency_matrix = generate_random_symmetric_complete_graph_adjacency_matrix(no_of_nodes, 10)

    # print(pd.DataFrame(adjacency_matrix))
    # path_indexes = stsp_nearest_neighbour(adjacency_matrix, max_cost)

    # print(path_indexes)
    # display_matplotlib_comparison(nodes, path_indexes, value_range)
    # display_networkx(adjacency_matrix, no_of_nodes, path_indexes)









