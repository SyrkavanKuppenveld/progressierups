from code.classes import Graph, Gate, Chip
from code.visualization import Chip_Visualization

if __name__ == "__main__":

    print_file = "example/print_0.csv"
    netlist_file = "example/netlist_1.csv"

    graph = Graph(print_file, netlist_file)

    # print_file = "gates&netlists/chip_2/print_2.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_9.csv"

    layers = 0
    chip = Chip(graph.gates, graph.connections, 0)

    

    wire = chip.construct_wirePath()
    # path = wire.path()
    # wire.get_wire_units()

    visualise_chip(graph.gates, wire)
    # chip.visualise_chip()