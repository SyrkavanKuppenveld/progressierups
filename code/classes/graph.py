import csv
import itertools 
from code.classes.gates import Gate
from code.classes.node import Node

class Graph():
    """
    Creates a Graph object that represents the chip grid and has the gates and 
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

        self.print_file = print_file
        self.netlist_file = netlist_file
        self.layers = layers
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
        for x, y, z in itertools.product(range(self.x_max + 1), range(self.y_max + 1), range(self.z_max + 1)):
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

    def getGateNeighbours(self, density, node, count, radius):
        """
        Recursively looks at all neighbors within a given radius of the respective gate 
        gate (="node"), and returns theneighbors that are a gate in a set.
    
        Parameters
        ----------
        density : set
                A set that is to be filled with neighbouring gates.
        node : a Node Object
                A Node Object of the gate-coordinate whose neighboring gates are to be retrieved.
        count : int
                An integers that keeps track of the recursion depth.
        radius : int
                An integer that specifies the depth of the recursion.

        Returns
        -------
        set
            A set of neighboring gates that lie within the given radius.

        """
        
        densitySet = density

        # Recursively get neighboring gates within radius distance
        if count < radius:
            count += 1
            # Check if neighbours are gates, if True append them to the density set
            for neighbor in node.neighbors:
                if neighbor.isgate:
                    densitySet.add(neighbor)
                    return densitySet
                
                # Update the node and resume recursion
                node = neighbor
                self.getGateNeighbours(densitySet, node, count, radius)
        
        return densitySet


    def getGateDensities(self):
        """
        Retrieves and returns a dictionary of gates with their "gate-density" (=number of gates
        in a pre-specified radius).

        Returns
        -------
        dict
                A dictionary of gates (=key) and their gate-density (=value).
        """

        gateDensities = {}

        for gate in self.gates:

            # Get corresponding node of the gate
            coords = self.gates[gate].xcoord, self.gates[gate].ycoord, self.gates[gate].zcoord
            node = self.nodes[coords]

            # Store gates that are within the pre-specified radius of the current gate
            density = set()

            # Determine radius (recursion depth)
            count = 0
            radius = 3

            # Get gate-density of the current gate and append it to the gateDensities dictionary
            density = self.getGateNeighbours(density, node, count, radius)
            gateDensities[gate] = len(density) - 1
        
        return gateDensities

    def getConnectionDistance(self, order):
        """
        Returns list with connection ordered based on the distances between gates.

        Parameters
        ----------
        order: a bool
                True if order is from max to min, False if order is from min to max.
        
        Returns
        -------
        list
                A list with connection ordered based on the distances between gates.
        """

        mdist = []

        # Compute Manhattan Distance between all connections in netlist
        for connection in self.netlist:

            # Get corresponding gate objects
            gate_a = self.gates[connection[0]]
            gate_b = self.gates[connection[1]]

            # Compute Manhattan Distance
            x_dist = abs(gate_a.xcoord - gate_b.xcoord)
            y_dist = abs(gate_a.ycoord - gate_b.ycoord)
            z_dist = abs(gate_a.zcoord - gate_b.zcoord)
            total_dist = x_dist + y_dist + z_dist

            # Append tuple with connection and Manhattan Distance
            mdist.append((connection, total_dist))
            
        # Sort connections based on order
        connections_sorted = sorted(mdist, key=lambda x:x[1], reverse=order)
        
        return [connection[0] for connection in connections_sorted]

    def ClearGraph(self):
        """
        Cleans a Graph Object.
        """

        self.gates = self.load_gates(self.print_file)
        self.connections, self.netlist = self.load_connections(self.netlist_file)
        self.x_max, self.y_max, self.z_max = self.grid_coords(self.layers)
        self.nodes = self.generate_nodes()
        self.generate_neighbors()
        self.set_gate_status()



        

