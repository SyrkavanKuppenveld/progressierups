from code.classes import Gate, Chip

if __name__ == "__main__":

    print_file = "example/print_0.csv"
    netlist_file = "example/netlist_1.csv"

    chip = Chip(print_file, netlist_file)

    gateConnections = chip.load_gateConnections(netlist_file)
    print(gateConnections)

    gate = chip.load_gates(print_file)
    print(gate)

    grid = chip.get_grid()
    print(grid)