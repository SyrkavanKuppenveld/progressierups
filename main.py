import code.classes as cs
import code.algorithms_revised as alg
from code.visualization.visualize import ChipVisualization
import helpers as hlp
import csv
import sys

def main():
    """
    Runs the user interface of the program for running the algorithms.
    """

    # Clear terminal
    sys.stderr.write("\x1b[2J\x1b[H")

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

    print()

    # Prompt user for heuristics if possible for algorithm choice
    if algorithm != 0:
        heuristic = hlp.uif.heuristic_input(netlist, algorithm)
        if heuristic < 3:
            connections, run_approach = hlp.uif.heuristic_order_input(chip, heuristic, graph)
        else:
            connections, run_approach = hlp.uif.heuristic_extention(chip, graph)

    print()

    # Instantiate algorithm according to user's input
    if algorithm == 0:
        algo = alg.Random(graph)
    elif algorithm == 1:
        algo = alg.Greedy(graph, connections, run_approach)
    elif algorithm == 2 and heuristic == 3:
        algo = alg.GreedyLookAheadCosts(graph, connections, run_approach)
    elif algorithm == 2:
        algo = alg.GreedyLookAhead(graph, connections, run_approach)
    elif algorithm == 3:
        algo = alg.HillClimber(graph)
    
    # Run algorithm
    print("Running Algorithm...")
    print()
    wire_path = algo.run()
    print("Algorithm completed!\n")

    # Visualize and or save algorithm results based on user's input
    hlp.uif.visualize_save_results(graph, wire_path)

    # Create output file
    with open("output.csv", 'w', newline='') as output_file:
        costs = algo.wire.compute_costs()
        hlp.save_csv(netlist_file, output_file, wire_path, costs)
    print()

    rerun = input("Would you like to run another algorithm? (y/n)\n")
    if rerun == 'y':
        sys.stderr.write("\x1b[2J\x1b[H")
        main()

if __name__ == "__main__":
    main()