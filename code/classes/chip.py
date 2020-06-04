import csv
from code.classes import Gate

class Chip():
    def __init__(self, print_file, netlist_file):
        self.gates = load_gates(print_file)
        self.gateConnections = load_gateConnections(netlist_file)
        self.grid = []
        self.wire = []

    def load_gates(self, source_file):
        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:

            # Initialize csv dictreader
            reader = csv.DictReader(input_file)

            # Iterate over lines in reader
            for i, row in enumerate(reader):
                    
                    # Store gate information
                    gateID, gateLetter, xcoord, ycoord = (i, row[0], row[1], row[2])

                    # Initialize Gate object
                    gate = Gate(gateID, gateLetter, xcoord, ycoord)

                    # Add gate to gates dict with gateID as key
                    gates[gateID] = gate
        
        return gates

    def load_gateConnections(self, source_file):
        connections = []

        # Parse netlist information
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                # Store connections
                    connections.append(tuple(row))

        return connections