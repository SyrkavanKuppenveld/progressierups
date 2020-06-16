import csv
import itertools 
from code.classes.gates import Gate
from code.classes.node import Node

class Graph():
    """
    Creates a Graph object that represents the chip grid and has the gates and the 
    netlists as attributes.
    """

    def __init__(self, print_file, netlist_file, layers=7):
        """
        Initializes a Graph object.
        
        parameters
        ----------
        print_file: a csv file
                A csv file containing the gates and their coordinates.
        
        netlist_file: a csv file
                A csv file containing a netlist.

        layers: int
                The number of layers of the chip.
        """

        self.gates = self.load_gates(print_file)
        self.connections, self.netlist = self.load_connections(netlist_file)
        self.x_max, self.y_max, self.z_max = self.grid_coords(layers)
        self.nodes = self.generate_nodes()
        self.generate_neighbors()
        self.set_gate_status()

    def load_gates(self, print_file):
        """
        Returns dictionary with all gate objects.

        parameters
        ----------
        print_file: a csv file
                A csv file containing the gates and their coordinates.
        
        returns
        -------
        dict
                A dictionary with gate coordinates as key and the corresponding Gate 
                object als value.
        """

        gates = {}

        # Open and read input_file
        with open(print_file, newline='') as input_file:
            reader = csv.DictReader(input_file)

            # Instanciate Gate objects and add to dictionary with chip as key
            for row in reader:
                gate = Gate(int(row['chip']), int(row['x']), int(row['y']))
                gates[int(row['chip'])] = gate

        return gates

    def load_connections(self, netlist_file):
        """
        Returns dictionary with gate connections.

        parameters
        ----------
        netlist_file: a csv file
                A csv file containing a netlist.

        returns
        -------
        dict
                A dictionary containing the Gate object as key and set containing the 
                Gate objects to which it needs te be connected.
        """

        connections = {}
        netlist = set()

        # Parse netlist information
        with open(netlist_file, newline='') as input_file:
            reader = csv.DictReader(input_file)

            # Store connections in list
            for row in reader:
                
                # Get corresponding gate objects
                a, b = int(row['chip_a']), int(row['chip_b'])
                netlist.add((a, b))
                gate_a, gate_b = self.gates[a], self.gates[b]

                # Create connections dictionary
                iter_list = [(gate_a, gate_b), (gate_b, gate_a)]
                for gates in iter_list:
                    if gates[0] not in connections:
                        connections[gates[0]] = {gates[1]}
                    else:
                        connections[gates[0]].add(gates[1])
    
        return connections, netlist

    def grid_coords(self, layers):
        """
        Returns the max coordinates of the grid.
        
        Paramaters
        ----------
        layers: int
                The number of layers of the chip.

        """

        gates = list(self.gates.values())
        x_max = max(gate.xcoord for gate in gates) + 1
        y_max = max(gate.ycoord for gate in gates) + 1
        z_max = layers

        return x_max, y_max, z_max

    def generate_nodes(self):
        """
        Returns dict with all nodes in grid.

        Returns
        -------
        dict
                A dictionary containing the coordinates of the grid as keys and the Node 
                objects as values.
        """
        
        nodes = {}

        # Generate all possible coordinates and create dict entry with coord as key
        for x, y, z in itertools.product(range(self.x_max + 1), range(self.y_max + 1), range(self.z_max)):
            coords = x, y, z
            nodes[coords] = Node(coords)

        return nodes

    def generate_neighbors(self):
        """
        Generates and adds all possible neighbors to nodes.
        """

        # Iterate over all nodes
        for node in self.nodes:
            
            # Generate all possible neighbors 
            for i, j, k in itertools.product(range(-1, 2), range(-1, 2), range(-1, 2)):
                x, y, z = self.nodes[node].xcoord, self.nodes[node].ycoord, self.nodes[node].zcoord
                neighbor = x + i, y + j, z + k

                # Only add existing neighbors
                diff_x = abs(x - neighbor[0])
                diff_y = abs(y - neighbor[1])
                diff_z = abs(z - neighbor[2])
                diff_total = diff_x + diff_y + diff_z
                if neighbor in self.nodes and diff_total == 1 and diff_x < 2 and diff_y < 2 and diff_z < 2:
                    self.nodes[node].add_neighbor(self.nodes[neighbor])
                
    def set_gate_status(self):
        """
        Sets isgate to True for all nodes containing a gate.
        """

        for gate in self.gates:
            coords = self.gates[gate].xcoord, self.gates[gate].ycoord, self.gates[gate].zcoord 
            self.nodes[coords].set_isgate()
