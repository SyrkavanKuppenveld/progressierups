from code.classes import Graph
from code.algorithms_revised import *
from code.visualization.visualize import ChipVisualization
from helpers import save_csv
import time
import csv
import sys


if __name__ == "__main__":

    # Prompt user for chip
    chip = int(input('Choose a chip: 0, 1 or 2?\n'))
    print()

    # Prompt user for netlist
    if chip == 0:
        netlist = int(input('Choose a netlist: 1, 2 or 3?\n'))
    elif chip == 1:
        netlist = int(input('Choose a netlist: 4, 5 or 6?\n'))
    else:
        netlist = int(input('Choose a netlist: 7, 8 or 9?\n'))
    print()

    # Determine print and netlist file based on user input
    print_file = f"gates&netlists/chip_{chip}/print_{chip}.csv"
    netlist_file = f"gates&netlists/chip_{chip}/netlist_{netlist}.csv"

    # Instantiate Graph object
    graph = Graph(print_file, netlist_file)

    # Prompt user for algorithm
    algorithm = int(input("Which algorithm would you like to run?\n> 0 = Random\n> 1 = Greedy\n> 2 = Greedy Look Ahead\n> 3 = Greedy Look Ahead Costs\n> 4 = Hillclimber\n"))
    print()
 
    # Prompt user for heuristics if possible for algorithm choice
    if algorithm != 0:
        # Prompt user for heuristic 
        heuristic = int(input("Which heuristic would you like to implement?\n> 0 = none\n> 1 = gate density\n> 2 = connnection distance\n"))
        print()

        # Prompt user for order heuristic list
        if heuristic != 0:
            order = bool(input("How would you like to implement the heuristic?\n> 0 = min-max\n> 1 = max-min\n"))
            print()

            # Instantiate connection list based on heuristic and in correct order
            if heuristic == 1:

                # Set density radius based on chip
                if chip == 0:
                    density_radius = 3
                else:
                    density_radius = 5

                # Generate connection list
                connections = graph.get_gate_densities(order, density_radius)

                # Set approach to False
                run_approach = False
            elif heuristic == 2:

                # Generate connection list
                connections = graph.get_connection_distance(order)

                # Set approach to True
                run_approach == True
        else:
            # Generate connection list
            connections = list(graph.netlist)

            # Set run aproach to True
            run_approach = True

    # Instantiate algorithm according to user's input
    if algorithm == 0:
        algo = Random(graph)
    elif algorithm == 1:
        algo = Greedy(graph, connections, run_approach)
    elif algorithm == 2:
        algo = GreedyLookAhead(graph, connections, run_approach)
    elif algorithm == 3:
        algo = GreedyLookAheadCosts(graph, connections, run_approach)
    elif algorithm == 4:
        algo = HillClimber(graph)
    
    # Run algorithm
    print("Running Algorithm...")
    print()
    wire_path = algo.run()
    print("Algorithm completed!\n")

    # Visualize algorithm results based on user's input
    show_visualization = input("Would you like to visualize the results? (y/n)\n")
    if show_visualization == 'y':
        visualisation = ChipVisualization(graph.gates, wire_path)
        visualisation.run()
    print()

    # Create output file
    with open("output.csv", 'w', newline='') as output_file:
        costs = algo.wire.compute_costs()
        save_csv(netlist_file, output_file, wire_path, costs)
    


