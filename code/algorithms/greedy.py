import numpy as numpy
from collections import Counter
from scipy.spatial import distance

class Greedy():
    """ Class that creates wires according to the shortest Manhattan Distance.
    
    The algorithm starts with building wires between the gate with number "1" as
    ID and its connections. It will continue building connections according to the 
    ID-numbers of the gates. It will first walk along the x-dimension and 
    subsequently along the y-dimension of the chip.
    ********************************************************************************
    """
    
    def __init__(self, connections, gates):
        self.connections = connections
        # self.gates = gates

        # Store wire paths (key = tuple of gate duo, value = list of coordinates)
        self.total_path = {}

        # Stores connections that have already been made
        self.completed_connections = set()

    def determine_gate_order(self):
        ordered_gates = []
        for gate in self.connections:
            ordered_gates.append((gate.gateID, gate))

        ordered_gates = sorted(ordered_gates, key=lambda x:x[0])

        return ordered_gates

    def compute_steps(self, current_gate_x, current_gate_y, connected_gate_x, connected_gate_y):
        steps_x = abs(current_gate_x - connected_gate_x)
        steps_y = abs(current_gate_y - connected_gate_y)

        return steps_x, steps_y

    def compute_relative_distances(self, current_gate_x, current_gate_y, connected_gate_x, connected_gate_y):
        relative_dist_x = connected_gate_x - current_gate_x
        relative_dist_y = connected_gate_y - current_gate_y

        return relative_dist_x, relative_dist_y


    def create_path(self, start_coordinates, relative_dist_x, relative_dist_y, steps_x, steps_y):

        path = []
        x_coord, y_coord = start_coordinates[0], start_coordinates[1]

        # Walk along the x-dimension
        for i in range(steps_x):
            if relative_dist_x > 0:
                x_coord += 1
            if relative_dist_x < 0:
                x_coord -= 1
            current_coords = (x_coord, y_coord)
            path.append(current_coords)

        # Walk along the y-dimension
        for i in range(steps_y):
            if relative_dist_y > 0:
                y_coord += 1
            if relative_dist_y < 0:
                y_coord -= 1
            current_coords = (x_coord, y_coord)
            path.append(current_coords)
        
        return path


    def run(self):
        """Returns wire path."""

        # for gate in self.connections:
        #     print(type(gate))
            # for connection in self.connections[gate]:
            #     print(type(connection))

        # Get a list of gates ordered by ID
        gate_order = self.determine_gate_order()
        # print(gate_order)

        # Build wire paths
        for index, gate in enumerate(gate_order):
            current_gateID, current_gateObject = gate
            # print("gate")
            # print(type(current_gateObject))
            # Create path for each connection of the current gate
            for connection in self.connections[current_gateObject]:
                connected_gateObject = connection
                connected_gateID = connected_gateObject.gateID
                
                current_path = []
        
                # Determine gate duo (= tuple)
                gate_duo = tuple(sorted([current_gateID, connected_gateID]))

                # Do not continue if a path between the current and connected gate already exists
                if gate_duo in self.completed_connections:
                    break

                # Get coordinates
                current_gate_x, current_gate_y = current_gateObject.xcoord, current_gateObject.ycoord
                connected_gate_x, connected_gate_y  = connected_gateObject.xcoord, connected_gateObject.ycoord 
                start_coordinates = (current_gate_x, current_gate_y)

                # Add start coordinates to the current path
                current_path.append(start_coordinates)

                # Compute steps
                steps_x, steps_y = self.compute_steps(current_gate_x, current_gate_y, connected_gate_x, connected_gate_y)

                # Compute relative distances
                relative_dist_x, relative_dist_y = self.compute_relative_distances(current_gate_x, current_gate_y, connected_gate_x, connected_gate_y)

                # Create path
                current_path_coordinates = self.create_path(start_coordinates, relative_dist_x, relative_dist_y, steps_x, steps_y)
                print(current_path_coordinates)
                # print(index)

                # Append current path to the total path
                self.total_path[gate_duo] = current_path_coordinates

                # Update the completed connections set
                self.completed_connections.add(gate_duo)

