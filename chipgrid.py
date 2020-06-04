import csv 
import numpy as np



class ChipGrid():
    """Initialize the Chip Grid structure."""

    def __init__(self, print_0, netlist_1):
        """Reads configuration files."""

        self.gates = []

        # Parse gate information coordinates
        with open(print_0, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                # Store 0) gatenumber, 1) gateletter and its coordinates: 2) x, 3) y
                if i > 0:
                    gate = (i, row[0], row[1], row[2])
                    self.gates.append(gate)

        self.connections = []

        # Open and read file containing netlist
        with open(netlist_1, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i > 0:
                    self.connections.append(tuple(row))

    def grid(self):
        pass
        
    def restrictions(self):
        """ Returns obligatory inter-gate connections"""
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
            
            gateRestrictions[gateNumber] = gateConnections


        return(gateRestrictions)

    
    
    

if __name__ == "__main__":

    print_file = "example/exprint_0.csv"
    netlist_file = "example/netlist_1.csv"

    chipgrid = ChipGrid(print_file, netlist_file)

    # grid_x, grid_y = chipgrid.grid()

    # print(grid_x)
    # print(grid_y)

    gateRestrictions = chipgrid.restrictions()
    print(gateRestrictions)