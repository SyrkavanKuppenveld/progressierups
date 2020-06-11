from code.classes import Gate
import csv
from math import sqrt


class Graph():
    """Graph datastructure"""

    def __init__(self, print_file, netlist_file):
        """Initialize Graph object."""

        self.gates = self.load_gates(print_file)
        self.connections = self.load_netlist(netlist_file)
        self.compute_distance()

    def load_gates(self, source_file):
        """Returns dictionary with all gate objects."""

        gates = {}

        # Open and read input_file
        with open(source_file, newline='') as input_file:

            # Initialize csv dictreader
            reader = csv.DictReader(input_file)

            # Iterate over lines in reader
            for gateID, row in enumerate(reader, 1):

                # Instanciate Gate object
                gate = Gate(gateID, row['chip'], row['x'], row['y'])

                # Add gate to gates dict with gateID as key
                gates[gateID] = gate    

        return gates


    def load_netlist(self, source_file):
        """Returns list with gate connections."""

        connections = {}

        # Parse netlist information
        with open(source_file, newline='') as input_file:
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

    def compute_distance(self):
        """Computes the distance to other gates."""

        # Iterate over the gates
        for gate in self.gates:
            dist = []

            # Iterate over the neighbors
            for neighbor in self.gates:

                # Assign gate coordinates
                gate_x, gate_y = self.gates[gate].xcoord, self.gates[gate].ycoord

                # Ensure that neighbor is not the current gate
                if neighbor is not gate:

                    # Assign neigbhors coordinates
                    neighbor_x, neighbor_y = self.gates[neighbor].xcoord, self.gates[neighbor].ycoord

                    # Compute Manhattan Distance
                    mdist= abs(gate_x - neighbor_x) + abs(gate_y - neighbor_y)
                    dist.append(mdist)
            
            # Instantiate gate distance and density
            self.gates[gate].get_distance(dist)
