import csv 
import numpy as np



class ChipGrid():
    """Provides the Chip Object."""

    def __init__(self, print_0, netlist_1):
        """ Initializes chip with the configuration files.

        Parameters
        ----------
        gates : list of gates (tuples: 0. gatenumber, 1. gateletter, 2. x-coordinate and 3. y-coordinate)
        connections :list of connected gates (tuples: 0. chip_a and 1. chip_b)
        """

        self.gates = []

        # Parse gate information coordinates
        with open(print_0, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                # Store gate information
                if i > 0:
                    gate = (i, row[0], row[1], row[2])
                    self.gates.append(gate)

        self.connections = []

        # Parse netlist information
        with open(netlist_1, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                # Store connections
                if i > 0:
                    self.connections.append(tuple(row))

    def grid(self):
        pass
        
    def restrictions(self):
        """ Identifies and returns gateRestrictions.
        
        Return
        ------
        gateRestrictions : dictionary of gates (key = gateNumber (int)) with it's connected gates (value: list of gateNumbers)
        """

        gateRestrictions = {}

        # Acquire connections per gate
        for gate in self.gates:
            gateNumber = gate[0]
            gateConnections = []
            # Check if connection is belongs to the respective gate
            for connection in self.connections:
                # If so, add connected gate to the gateRestrictions dictionary
                if str(gateNumber) in connection:
                    if connection[0] != str(gateNumber):
                        gateConnections.append(connection[0])
                    else:
                        gateConnections.append(connection[1])
            
            # Store gate connections
            gateRestrictions[gateNumber] = gateConnections


        return gateRestrictions

    
    
    

if __name__ == "__main__":

    print_file = "example/exprint_0.csv"
    netlist_file = "example/netlist_1.csv"

    chipgrid = ChipGrid(print_file, netlist_file)

    gateRestrictions = chipgrid.restrictions()
    print(gateRestrictions)