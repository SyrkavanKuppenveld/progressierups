import csv
from code.classes.gates import Gate
from code.classes.grid import Grid

class Chip():
    def __init__(self, print_file, netlist_file):
        self.gates = self.load_gates(print_file)
        self.gateConnections = self.load_gateConnections(netlist_file)
        self.grid = self.get_grid()
        self.wire = []

    def load_gates(self, source_file):
        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:

            # Initialize csv dictreader
            reader = csv.DictReader(input_file)

            # Iterate over lines in reader
            for i, row in enumerate(reader, 1):

                    # Initialize Gate object
                    gate = Gate(i, row['chip'], row['x'], row['y'])

                    # Add gate to gates dict with gateID as key
                    gates[i] = gate
        
        return gates

    def load_gateConnections(self, source_file):
        connections = []

        # Parse netlist information
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                # Store connections (as a tuple)
                    connections.append((row['chip_a'], row['chip_b']))

        return connections

    def get_grid(self):

        grid = Grid(self.gates)
        
        return grid.filled_grid

