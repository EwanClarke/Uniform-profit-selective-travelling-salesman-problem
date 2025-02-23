from algorithms.cheapest_insertion import stsp_cheapest_insertion
from algorithms.nearest_neighbour_adaption import stsp_nearest_neighbour
from algorithms.ant_colony_optimisation import stsp_ant_colony_optimisation
from graph_visualisation import construct_networkx_visualisation_positional
from utils import tour_length_adjacency_matrix
from exact_method import stsp_exact_algorithm
from generate_problem import random_path, calculate_complete_graph_adjacency_matrix

from random import randrange
import tsplib95
import networkx as nx
from matplotlib import pyplot as plt
import argparse
from time import perf_counter_ns

if __name__ == '__main__':
    algorithm_choices = ["cheapest_insertion", "nearest_neighbour", "ant_colony", "branch_and_bound"]
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--problem", help="file name of problem in problems folder to solve, random problem "
                                               "generated if not selected", type=str)
    group.add_argument("-r", "--random", help="generates a random problem with the specified number of nodes", type=int)
    parser.add_argument("-b", "--budget", default=200, help="traversal budget for the problem", type=int)
    parser.add_argument("-a", "--algorithms", help="algorithm(s) to run the problem through", nargs='+',
                        default=algorithm_choices[0], choices=algorithm_choices)
    parser.add_argument("-c", "--compare", help="show comparison of all algorithms run", action="store_true")
    parser.add_argument("-d", "--display", help="display visualisations of algorithm results", action="store_true")
    args = parser.parse_args()

    if args.problem is None:
        no_of_nodes = args.random if args.random is not None else randrange(50, 500)
        value_range = 200
        random_problem = random_path(no_of_nodes, value_range)
        pos = {}
        for node in random_problem:
            pos[node.get_node_id()] = node.get_coords()

        adjacency_matrix = calculate_complete_graph_adjacency_matrix(random_problem).to_numpy()
        print(f"Graph generated with {no_of_nodes} nodes")
    else:

        problem = tsplib95.load(f"problems/{args.problem}")
        print(f"Problem {args.problem} loaded successfully")

        pos = dict(zip(range(0, len(list(problem.get_nodes()))), list(problem.node_coords.values())))
        G = problem.get_graph()
        adjacency_matrix = nx.to_numpy_array(G)
        no_of_nodes = problem.dimension

    max_cost = args.budget

    if isinstance(args.algorithms, list):
        algorithms = args.algorithms
    else:
        algorithms = [args.algorithms]
    runtimes = {}
    results = {}
    for algorithm in algorithms:
        print(f"running {algorithm.replace("_", " ")} algorithm")
        start = perf_counter_ns()
        match algorithm:
            case "cheapest_insertion":
                results[algorithm] = stsp_cheapest_insertion(adjacency_matrix, max_cost)
            case "nearest_neighbour":
                results[algorithm] = stsp_nearest_neighbour(adjacency_matrix, max_cost)
            case "ant_colony":
                results[algorithm] = stsp_ant_colony_optimisation(adjacency_matrix, max_cost)
            case "branch_and_bound":
                results[algorithm] = stsp_exact_algorithm(adjacency_matrix, max_cost)
        runtimes[algorithm] = perf_counter_ns() - start

    if args.compare:
        print("")
        print(" Problem information ".center(40, "-"))
        print(f"number of nodes: {no_of_nodes}")
        print(f"traversal budget: {max_cost}")
        print("")

        for algorithm in algorithms:
            print(f" {algorithm.replace("_", " ")} data ".center(40, "-"))
            print(f"runtime: {runtimes[algorithm]:,d} ns")
            print(f"number of nodes visited: {len(results[algorithm])-1}")
            print(f"length of path: {tour_length_adjacency_matrix(adjacency_matrix, results[algorithm])}")
            print("")
        pass

    if args.display:
        for algorithm in algorithms:
            print(f"constructing {algorithm.replace("_", " ")} results visualisation")
            plt.figure(algorithm)
            construct_networkx_visualisation_positional(adjacency_matrix, no_of_nodes, results[algorithm], pos)
        print("displaying results visualisation(s)")
        plt.show()
