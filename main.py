from code.classes import Gate, Chip

if __name__ == "__main__":

    print_file = "example/print_0.csv"
    netlist_file = "example/netlist_1.csv"

    # print_file = "gates&netlists/chip_2/print_2.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_9.csv"

    chip = Chip(print_file, netlist_file)

    gateConnections = chip.load_netlist(netlist_file)
    print(gateConnections)

    grid = chip.get_grid()
    print(grid)

    wire = chip.construct_wirePath()
    # path = wire.path()
    # wire.get_wire_units()

    chip.visualise_chip()