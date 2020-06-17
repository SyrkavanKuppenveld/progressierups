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
        
        Parameters
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

        Parameters
        ----------
        print_file: a csv file
                A csv file containing the gates and their coordinates.
        
        Returns
        -------
        dict
                A dictionary with gate coordinates as key and the corresponding Gate 
                object als value.
        """

        gates = {}

        # Open and read input_file
        with open(print_file, newline='') as input_file:
            reader = csv.DictReader(input_file)

            # Instantiate Gate objects and add them to dictionary with chip as key
            for row in reader:
                gate = Gate(int(row['chip']), int(row['x']), int(row['y']))
                gates[int(row['chip'])] = gate

        return gates

    def load_connections(self, netlist_file):
        """
        Returns dictionary with gate connections.

        Parameters
        ----------
        netlist_file: a csv file
                A csv file containing a netlist.

        Returns
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
        Returns dict with all nodes present in the 3D grid.

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

    def compute_densities(self, radius):
        """
        Returns a orded list with Gate objects sorted form max to min density.

        Parameters
        ----------
        radius: int
                The radius for which the density should be computed.

        Returns
        -------
        list 
                A list with Gate objects sorted from max to min density.
        """

        gate_density = []

        # Compute the density for all gates
        for gate in self.gates:

            # Get x and y coordinates gate
            x, y = self.gates[gate].xcoord, self.gates[gate].ycoord 

            neighbors = set()

            # Generate all posible neighbors and add to set
            for i, j in itertools.product(range(-radius, radius + 1), range(-radius, radius + 1)):
                x_neighbor = x + i
                y_neighbor = y + j
                z_neighbor = 0
                neighbor_coords = x_neighbor, y_neighbor, z_neighbor
                if neighbor_coords in self.nodes:
                    neighbors.add(self.nodes[neighbor_coords])

            # Compute number of nodes that contain a gate
            density = 0
            for neighbor in neighbors:
                if neighbor.isgate:
                    density += 1
            
            # Append gate and density to list
            gate_density.append((gate, density))
        
        # Sort gates from max to min density
        sorted_density = sorted(gate_density, key=lambda x:x[1], reverse=True)

        return sorted_density
        

def compute_density(self, radius=4):
    
    gate_density = []

    for gate in self.gates:

        # Get corresponding node
        coords = self.gates[gate].xcoord, self.gates[gate].ycoord, self.gates[gate].zcoord
        node = self.nodes[coords]

        density = set()

        for neighbor in node.neighbors:
            if neighbor.isgate:
                density.add(neighbor)

            for neighbor_1 in neighbor.neighbors:
                if neighbor_1.isgate:
                    density.add(neighbor_1)
            
                for neighbor_2 in neighbor_1.neighbors:
                    if neighbor_2.isgate:
                        density.add(neighbor_2)

                    for neighbor_3 in neighbor_2.neighbors:
                        if neighbor_3.isgate:
                            density.add(neighbor_3)

                        for neighbor_4 in neighbor_3.neighbors:
                            if neighbor_4.isgate:
                                density.add(neighbor_4)

                            for neighbor_5 in neighbor_4.neighbors:
                                if neighbor_5.isgate:
                                    density.add(neighbor_5)

                                for neighbor_6 in neighbor_5.neighbors:
                                    if neighbor_6.isgate:
                                        density.add(neighbor_6)

                                        for neighbor_7 in neighbor_6.neighbors:
                                            if neighbor_7.isgate:
                                                density.add(neighbor_7)

    # Sort gates from max to min density
    sorted_density = sorted(gate_density, key=lambda x:x[1], reverse=True)

    return sorted_density








# def get_recurs_neighbours(self, density, node, count, base):
#     density_set = density
#     if count < base:
#         for neighbour in node.neighbours:
#             if not neighbour.isgate():
#                 density_set.add(neighbour)
#                 count += 1
#                 return density
            
#             node = neighbour
#             self.get_recurs_neighbours(density_set, node, count, base)


# def recursive_density(self, radius=4):
    
#     gate_density = []

#     for gate in self.gates:

#         # Get corresponding node
#         coords = self.gates[gate].xcoord, self.gates[gate].ycoord, self.gates[gate].zcoord
#         node = self.nodes[coords]

#         density = set()

#         count = 0
#         base = 7
#         density = self.get_recurs_neighbours(density, node, count, base)
        

