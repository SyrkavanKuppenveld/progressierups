from code.classes import Gate, Chip

if __name__ == "__main__":

    print_file = "example/print_0.csv"
    netlist_file = "example/netlist_1.csv"

    chip = Chip(print_file, netlist_file)

    gateConnections = chip.load_gateConnections()
    print(gateConnections)