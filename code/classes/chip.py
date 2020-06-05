import csv
from code.classes.gates import Gate
from code.classes.grid import Grid
from code.classes.wire import Wire

class Chip():
    def __init__(self, print_file, netlist_file):
        self.netlist = self.load_netlist(netlist_file)
        self.gates = self.load_gates(print_file)
        self.grid = self.get_grid()
        self.wire = self.construct_wirePath

    def load_netlist(self, source_file):
        connections = []

        # Parse netlist information
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                # Store connections (as a tuple)
                    connections.append((int(row['chip_a']), int(row['chip_b'])))

        return connections
    
    def get_gateConnections(self, gateID):

        connections = {}

        # Iterate over all gate connections
        for connection in self.netlist:
            if gateID in connection:
                # Only store the connected gate and not the current gates' ID
                # Set the connected gateID as key with a default value of False corresponding with it's connection status
                if connection[0] != gateID:
                    connections[connection[0]] = False
                else:
                    connections[connection[1]] = False
        
        return connections
    
    def load_gates(self, source_file):
        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:

            # Initialize csv dictreader
            reader = csv.DictReader(input_file)

            # Iterate over lines in reader
            for i, row in enumerate(reader, 1):
                    
                    # Retrieve connections with the current gate
                    gateID = str(i)
                    connections = self.get_gateConnections(gateID)

                    # Initialize Gate object
                    gate = Gate(str(i), row['chip'], row['x'], row['y'], connections)

                    # Add gate to gates dict with gateID as key
                    gates[i] = gate

        print(gates)
        
        return gates

    def get_grid(self):

        grid = Grid(self.gates)
        
        return grid.filled_grid

    def construct_wirePath(self):
         
        wire = Wire(self.grid, self.gates, self.netlist)


        return wire

