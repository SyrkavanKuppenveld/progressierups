from code.classes import Gate
from code.classes.graph_new import Graph
from code.algorithms.eline_algo import Algorithm
from code.visualization import Chip_Visualization

if __name__ == "__main__":

    print_file = "example/print_0.csv"
    netlist_file = "example/netlist_1.csv"

    graph = Graph(print_file, netlist_file)

    # Perform Algorithm
    algo = Algorithm(graph)
    wire_path = algo.run()
    print(wire_path)

    visualisation = Chip_Visualization(graph.gates, wire_path)
    visualisation.run()
