from heuristics.cheapest_insertion import stsp_cheapest_insertion
from heuristics.nearest_neighbour_adaption import stsp_nearest_neighbour
from graph_visualisation import display_networkx_positional, display_matplotlib_comparison
from path_utilities import tour_length_adjacency_matrix
from exact_method import stsp_exact_algorithm
from generate_problem import random_path, calculate_complete_graph_adjacency_matrix
from random import randrange
import tsplib95
import networkx as nx
from matplotlib import pyplot as plt
import argparse
from time import perf_counter

if __name__ == '__main__':
    algorithm_choices = ["cheapest_insertion", "nearest_neighbour"]
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--problem", help="file name of problem in problems folder to solve, random problem "
                                               "generated if not selected", type=str)
    group.add_argument("-r", "--random", help="generates a random problem with the specified number of nodes", type=int)
    parser.add_argument("-b", "--budget", help="traversal budget for the problem", type=int)
    parser.add_argument("-a", "--algorithms", help="algorithm(s) to run the problem through", nargs='+',
                        default=algorithm_choices[0], choices=algorithm_choices)
    parser.add_argument("-c", "--compare", help="show comparison of all algorithms run", action="store_true")
    parser.add_argument("-d", "--display", help="display visualisations of algorithm results", action="store_true")
    parser.add_argument("-s", "--save", help="Save visualisations of algorithm results to provided filepath", type=str)
    args = parser.parse_args()

    if args.problem is None:
        no_of_nodes = randrange(50, 500)
        value_range = randrange(100, 200)
        random_problem = random_path(no_of_nodes, value_range)
        # work out pos from random problem
        adjacency_matrix = calculate_complete_graph_adjacency_matrix(random_problem)
        print(f"Graph generated with {no_of_nodes} nodes")
    else:
        try:
            problem = tsplib95.load(f"problems/{args.problem}") if args.problem is not None else None
            print(f"Problem {args.problem} loaded successfully")
        except FileNotFoundError:
            raise FileNotFoundError("File \"{args.problem}\" was not found")
        pos = dict(zip(range(0, len(list(problem.get_nodes()))), list(problem.node_coords.values())))
        G = problem.get_graph()
        adjacency_matrix = nx.to_numpy_array(G)

    max_cost = args.budget if args.budget is not None else 100

    if isinstance(args.algorithms, list):
        algorithms = args.algorithms
    else:
        algorithms = [args.algorithms]
    runtimes = {}
    results = {}
    for algorithm in algorithms:
        print(f"running {algorithm.replace("_", " ")} algorithm")
        start = perf_counter()
        match algorithm:
            case "cheapest_insertion":
                results[algorithm] = stsp_cheapest_insertion(adjacency_matrix, max_cost)
            case "nearest_neighbour":
                results[algorithm] = stsp_nearest_neighbour(adjacency_matrix, max_cost)
        runtimes[algorithm] = perf_counter() - start

    if args.compare is not None:
        pass

    if args.display is not None:
        for algorithm in algorithms:
            print(f"displaying {algorithm.replace("_", " ")} algorithm results visualisation")
            if args.problem is not None:
                display_networkx_positional(adjacency_matrix, len(adjacency_matrix), results[algorithm], pos)
            else:
                display_networkx_positional(adjacency_matrix, no_of_nodes, results[algorithm], pos)
