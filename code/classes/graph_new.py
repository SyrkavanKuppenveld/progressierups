import csv
import itertools 
from code.classes import Gate, Node

class Graph():

    def __init__(self, print_file, netlist_file, layers=7):
        """Initializes a Graph object."""

        self.gates = self.load_gates(print_file)
        self.connections = self.load_connections(netlist_file)
        self.x_max, self.y_max, self.z_max = self.grid_coords(layers)
        self.nodes = self.generate_nodes()
        self.generate_neighbors()
        self.set_gate_status()

    def load_gates(self, source_file):
        """Returns dictionary with all gate objects."""

        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:
            reader = csv.DictReader(input_file)

            # Instanciate Gate objects and add to dictionary with chip as key
            for row in reader:
                gate = Gate(int(row['chip']), int(row['x']), int(row['y']))
                gates[int(row['chip'])] = gate

        return gates

    def load_connections(self, netlist_file):
        """Returns dictionary with gate connections."""

        connections = {}

        # Parse netlist information
        with open(netlist_file, newline='') as input_file:
            reader = csv.DictReader(input_file)

            # Store connections in list
            for row in reader:
                
                # Get corresponding gate objects
                a, b = int(row['chip_a']), int(row['chip_b'])
                gate_a, gate_b = self.gates[a], self.gates[b]

                # Create connections dictionary
                iter_list = [(gate_a, gate_b), (gate_b, gate_a)]
                for gates in iter_list:
                    if gates[0] not in connections:
                        connections[gates[0]] = {gates[1]}
                    else:
                        connections[gates[0]].add(gates[1])
    
        return connections

    def grid_coords(self, layers):
        """Returns the max coordinates of the grid."""

        gates = list(self.gates.values())
        x_max = max(gate.xcoord for gate in gates) + 1
        y_max = max(gate.ycoord for gate in gates) + 1
        z_max = layers

        return x_max, y_max, z_max

    def generate_nodes(self):
        """Returns dict with all nodes in grid."""
        
        nodes = {}

        # Generate all possible coordinates and create dict entry with coord as key
        for x, y, z in itertools.product(range(self.x_max + 1), range(self.y_max + 1), range(self.z_max)):
            coords = x, y, z
            nodes[coords] = Node(coords)

        return nodes

    def generate_neighbors(self):
        """Generates and adds all possible neighbors to nodes."""

        # Iterate over all nodes
        for node in self.nodes:
            
            # Generate all possible neighbors 
            for i, j, k in itertools.product(range(-1, 2), range(-1, 2), range(-1, 2)):
                x, y, z = self.nodes[node].xcoord, self.nodes[node].ycoord, self.nodes[node].zcoord
                neighbor = x + i, y + j, z + k

                # Only add existing neighbors
                diff_x = abs(x - neighbor[0])
                diff_y = abs(y - neighbor[1])
                diff_z = abs(z 
                 - neighbor[2])
                diff_total = diff_x + diff_y + diff_z
                if neighbor in self.nodes and diff_total == 1 and diff_x < 2 and diff_y < 2 and diff_z < 2:
                    self.nodes[node].add_neighbor(self.nodes[neighbor])
                
    def set_gate_status(self):
        """Sets isgate to True for all nodes containing a gate."""

        for gate in self.gates:
            coords = self.gates[gate].xcoord, self.gates[gate].ycoord, self.gates[gate].zcoord 
            self.nodes[coords].set_isgate()
