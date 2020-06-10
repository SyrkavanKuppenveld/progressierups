from code.classes import Gate
import csv
from math import sqrt


class Graph():
    """Graph datastructure"""

    def __init__(self, print_file, netlist_file):
        """Initialize Graph object."""

        self.gates = self.load_gates(print_file)
        self.connections = self.load_netlist(netlist_file)

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

                # Make connections >> DIT KAN NETTER MBT DUPLICATED CODE!
                if gate_a not in connections:
                    connections[gate_a] = {gate_b}
                else:
                    connections[gate_a].add(gate_b)
                
                if gate_b not in connections:
                    connections[gate_b] = {gate_a}
                else:
                    connections[gate_b].add(gate_a)

        return connections

    def computeDensities(self):
        pass




    # def getDensity(self, gates):
    #     """Returns """

    #     k = round(sqrt(len(self.vertices)))

    #     density = {}

    #     for gate in self.vertices:

    #         dist = []

    #         for neighbor in self.vertices:

    #             if neighbor is not gate:
                    
    #                 # Get coordinates 
    #                 gate_x, gate_y = gates[gate].xcoord, gates[gate].ycoord
    #                 neighbor_x, neighbor_y = gates[neighbor].xcoord, gates[neighbor].ycoord

    #                 # Compute Manhattan Distance
    #                 mdist= abs(gate_x - neighbor_x) + abs(gate_y - neighbor_y)
    #                 dist.append(mdist)

    #         # Sum k lowest distances      
    #         k_min = sorted(dist)
    #         k_total = sum(k_min[0:k])
    #         density[gate] = k_total

    #     # Test prints
    #     print(k)
    #     print(density)



        

