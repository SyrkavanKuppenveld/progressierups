from gates import Gate
import csv

class Chip():
    def __init__(self, print_file, netlist_file):
        self.gates = load_gates(print_file)
        self.gateConnections = load_gateConnections(netlist_file)
        self.grid = []
        self.wire = []

    def load_gates(self, source_file):
        gates = []

        # Parse gate information coordinates
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)
            for i, row in enumerate(reader):
                # Store gate information
                    gateID, gateLetter, xcoord, ycoord = (i, row[0], row[1], row[2])
                    gate = Gate(gateID, gateLetter, xcoord, ycoord) # << hier een gate Object instantieren
                    gates.append(gate)
        
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