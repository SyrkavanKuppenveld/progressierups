import code.classes as cs
import code.algorithms as alg
from code.visualization.visualize import ChipVisualization
import helpers as hlp
import csv
import sys
import os

def main():
    """
    Runs the user interface of the program for running the algorithms.
    """

    # Clear terminal
    os.system('cls')

    # Prompt user for chip
    chip = hlp.uif.chip_input()
    print()

    # Prompt user for netlist
    netlist = hlp.uif.netlist_input(chip)
    print()

    # Determine print and netlist file based on user input
    print_file = f"gates&netlists/chip_{chip}/print_{chip}.csv"
    netlist_file = f"gates&netlists/chip_{chip}/netlist_{netlist}.csv"

    # Instantiate Graph object
    graph = cs.Graph(print_file, netlist_file)

    # Prompt user for algorithm
    algorithm = hlp.uif.algorithm_input(netlist)
    
    # If the Hillclimber algorithm is chosen, specify its workflow
    frequency = None
    start_state_flow = None 
    conversion_plot_flow = None
    if algorithm == 3 or algorithm == 4:
        frequency, start_state_flow, conversion_plot_flow = hlp.uif.get_hillclimber_flow(algorithm)

    # Only prompt user for heuristics if algorithm is not random (=0) and no hillclimber (=3 & 4)
    if algorithm != 0 and algorithm != 3 and algorithm != 4:
        heuristic = hlp.uif.heuristic_input(netlist, algorithm)
        if heuristic < 3:
            print()
            connections, run_approach = hlp.uif.heuristic_order_input(chip, netlist, algorithm, heuristic, graph)
        else:
            print()
            connections, run_approach = hlp.uif.heuristic_extention(chip, heuristic, graph)

    print()

    # Instantiate algorithm according to user's input
    if algorithm == 0:  
        algo = alg.Random(graph)
    elif algorithm == 1 and heuristic == 3:
        algo = alg.GreedyCosts(graph, connections, run_approach)
    elif algorithm == 1 and heuristic == 4:
        algo = alg.GreedyNoIntersect(graph, connections, run_approach)
    elif algorithm == 1 and heuristic == 5:
        algo = alg.GreedyWireJam(graph, connections, run_approach)
    elif algorithm == 1:
        algo = alg.Greedy(graph, connections, run_approach)
    elif algorithm == 2 and heuristic == 3:
        algo = alg.GreedyLookAheadCosts(graph, connections, run_approach)
    elif algorithm == 2 and heuristic == 4:
        algo = alg.GreedyNoIntersectLookAhead(graph, connections, run_approach)
    elif algorithm == 2 and heuristic == 5:
        algo = alg.GreedyLookAheadWireJam(graph, connections, run_approach)
    elif algorithm == 2:
        algo = alg.GreedyLookAhead(graph, connections, run_approach)
    elif algorithm == 3 or algorithm == 4:
        algo = alg.HillClimber(graph, frequency, start_state_flow, conversion_plot_flow, chip, netlist)

    # Run algorithm
    print("Running Algorithm...")
    print()
    wire_path = algo.run()
    print("\033[0;32m""Algorithm completed!\n""\033[0m")
    print()

    # Print wire costs if anything but a Hillclimber is run, since the Hillclimber
    # handles its own costst
    if algorithm < 3:
        wire_costs = algo.wire.compute_costs()
        print("\033[33m"f"Wire costs = {wire_costs}""\033[0m")
        print()

    # Visualize and or save algorithm results based on user's input
    hlp.uif.visualize_save_results(graph, wire_path)
    print()

    # Visualize and or save algorithm results based on user's input
    hlp.uif.heatmap_visualize_save(graph.nodes, algo.wire)
    print()

    # Create output file
    with open("output.csv", 'w', newline='') as output_file:
        costs = algo.wire.compute_costs()
        hlp.save_csv(netlist_file, output_file, wire_path, costs)
    print()

    # Restart or quit program
    print("\033[1m""Would you like to run another algorithm? (y/n)""\033[0m")
    rerun = input()
    if rerun == 'y':
        main()

if __name__ == "__main__":
    main()