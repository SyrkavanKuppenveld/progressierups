import csv
from code.classes.gates import Gate
from code.classes.grid import Grid
from code.classes.wire import Wire
from code.classes.graph import Graph

class Chip():
    def __init__(self, print_file, netlist_file):
        """Initialize Chip object."""

        self.netlist = self.load_netlist(netlist_file)
        self.connections = self.create_graph()
        self.gates = self.load_gates(print_file)
        self.grid = self.get_grid()
        self.wire = self.construct_wirePath

    def load_netlist(self, source_file):
        """Returns list with gate connections."""

        connections = []

           # Parse netlist information
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)
            
            # Store connections in list
            for row in reader:
                connections.append((int(row['chip_a']), int(row['chip_b'])))

        return connections


    def create_graph(self):
        """Returns graph with gates as key and the connections als values."""

        connections = Graph(self.netlist)
        
        return connections

    
    # DEZE FUNCTIE RETURN MOMENTEEL NOG EEN LEGE DICT, AANGEZIEN DIE NOOIT DOOR DE
    # IF STATEMENT HEENKOMT, IK WEET NIET PRECIES WAT DEZE NOU MOET DOEN DUS DAAR
    # MOETEN WE DAN NOG EVEN NAAR KIJKEN (Eline)
    def get_gateConnections(self, gateID):
        """Returns ."""

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
        """Returns dictionary with all gate objects."""

        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:

            # Initialize csv dictreader
            reader = csv.DictReader(input_file)

            # Iterate over lines in reader
            for i, row in enumerate(reader, 1):

                # Retrieve connections with the current gate
                gateID = str(i)

                # Initialize Gate object
                gate = Gate(str(i), row['chip'], row['x'], row['y'], self.connections.graph[i])

                # Add gate to gates dict with gateID as key
                gates[i] = gate    

        return gates

    def get_grid(self):
        """Returns chip grid with gates filled in."""

        grid = Grid(self.gates)
        
        return grid.filled_grid

    def construct_wirePath(self):
        """Returns constructed wire path."""
         
        wire = Wire(self.grid, self.gates, self.connections)


        return wire

    

