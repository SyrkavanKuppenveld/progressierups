from code.classes import Gate
import csv
from math import sqrt


class Graph():
    """Graph datastructure"""

    def __init__(self, print_file, netlist_file):
        """Initialize Graph object."""

        self.gates = self.load_gates(print_file)
        self.connections = self.load_netlist(netlist_file)
        self.density = self.compute_densities()

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

    def compute_densities(self):
        """Returns dictionary with gate densities."""

        density = {}

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
            
            # Create density 
            density[gate] = dist

        return density

    def get_densityMin(self):
        """Returns gate with lowest density."""

        # Compute number of gates and k
        num_gates = len(self.gates)
        k = round(sqrt(num_gates))

        min_dist = []

        # Sum k min distances and append for all gates
        for gate in self.density:
            dist_sorted = sorted(self.density[gate])
            k_total = sum(dist_sorted[0:k])
            min_dist.append((gate, k_total))

        # Sort max_dist from min to max
        min_dist = sorted(min_dist, key=lambda x: x[1])

        return min(min_dist)

    def get_densityMax(self):
        """Returns gate with lowest density."""

        # Compute number of gates and k
        num_gates = len(self.gates)
        k = round(sqrt(num_gates))

        max_dist = []

        # Sum k max distances and append for all gates
        for gate in self.density:
            dist_sorted = sorted(self.density[gate], reverse=False)
            k_total = sum(dist_sorted[0:k])
            max_dist.append((gate, k_total))

        # Sort max_dist from max to min
        max_dist = sorted(max_dist, key=lambda x: x[1])
        
        return max(max_dist)
        