import itertools
import csv
import code.classes as cs
import code.algorithms as alg


if __name__ == "__main__":

    # Generate all chip and nestlist combination
    for chip, netlist in itertools.product(range(0, 3), range(1, 4)):
        
        # Correct netlist for chip
        netlist += (chip * 3)

        # Break if netlist is higher than 4
        if netlist > 4:
            break
        
        # Determine print and netlist file based on user input
        print_file = f"gates&netlists/chip_{chip}/print_{chip}.csv"
        netlist_file = f"gates&netlists/chip_{chip}/netlist_{netlist}.csv"

        costs = []
        index = []

        # Open and write new file
        with open(f"results/algorithms/part1/no_inter_lookahead/netlist_{netlist}.csv", 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['index', 'costs'])

            # Run algorithm 100 times
            for i in range(1, 26):
                index.append(i)

                # Instantiate Graph object
                graph = cs.Graph(print_file, netlist_file)

                # Set density radius based on chip
                if chip == 0:
                    density_radius = 3
                else:
                    density_radius = 3

                # Set order to True
                order = True

                # Generate gate/connection order list
                order = list(graph.netlist)

                # Run algorithm
                algorithm = alg.GreedyNoIntersectLookAhead(graph, order, approach=True)
                algorithm.run()

                # Compute and append wire costs
                wire_costs = algorithm.wire.compute_costs()
                costs.append(wire_costs)

            # Write rows               
            writer.writerows(zip(index, costs))
