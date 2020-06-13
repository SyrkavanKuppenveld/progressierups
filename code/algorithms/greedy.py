# import numpy as numpy

from code.classes.node import Node
from code.visualization.visualize import Chip_Visualization

class Greedy():
    """ Class that creates wires according to the shortest Manhattan Distance.
    
    The algorithm starts with building wires between the gate with number "1" as
    ID and its connections. It will continue building connections according to the 
    ID-numbers of the gates. Paths to the gates' corresponding connection will also
    be made based upon the ID of the connected gate. It will first walk along the 
    x-dimension and subsequently along the y-dimension of the chip.
    ********************************************************************************
    """
    
    def __init__(self, graph):
        self.graph = graph
        
        # Store already connected gate-net-duo
        self.completed_connections = set()
        
        # Store wire paths (key = tuple of gate duo, value = list of coordinates)
        self.total_path = {}

    
    def determine_gate_order(self):
        ordered_gates = []
        
        for gate in self.graph.connections:
            ordered_gates.append((gate.gateID, gate))

        ordered_gates = sorted(ordered_gates, key=lambda x:x[0])
        
        return ordered_gates

    
    def compute_steps(self, current_gate_coords, connected_gate_coords):
        steps_x = abs(current_gate_coords[0] - connected_gate_coords[0])
        steps_y = abs(current_gate_coords[1] - connected_gate_coords[1])

        return steps_x, steps_y

    def compute_rel_Manhattandist(self, current_gate_coords, connected_gate_coords):
        relative_dist_x = connected_gate_coords[0] - current_gate_coords[0]
        relative_dist_y = connected_gate_coords[1] - current_gate_coords[1]

        return relative_dist_x, relative_dist_y
    
    def create_path(self, start_coordinates, relative_dist_x, relative_dist_y, connected_gate_coords):

        path = []
        x_coord, y_coord = start_coordinates[0], start_coordinates[1]
        
        # Since steps are made according to the Manhatten distance, the z_coordinate
        # will always be zero.
        z_coord = 0

        current_coords = start_coordinates
        goal_coords = connected_gate_coords

        # Walk along the x-dimension
        if relative_dist_x != 0:
            print(f"relative dist x: {relative_dist_x}")
            while current_coords[0] != goal_coords[0]:
                if relative_dist_x > 0:
                    x_coord += 1
                else:
                    x_coord -= 1
                current_coords = (x_coord, y_coord, z_coord)
                path.append(current_coords)

        # Walk along the y-dimension
        if relative_dist_y != 0:
            print(f"relative dist y: {relative_dist_y}")
            while current_coords[1] != goal_coords[1]:
                if relative_dist_y > 0:
                    y_coord += 1
                else:
                    y_coord -= 1
                current_coords = (x_coord, y_coord, z_coord)
                path.append(current_coords)

        return path
    
    def run(self):
        """Returns wire path."""

        # Get a list of gates ordered by ID
        gate_order = self.determine_gate_order()

        # Build wire paths
        for index, gate in enumerate(gate_order):

            current_gateID, current_gateObject = gate
            connections = list(self.graph.connections[current_gateObject])
            
            # Create path for each connection of the current gate
            for index, connection in enumerate(connections):
                connected_gateObject = connection
                connected_gateID = connected_gateObject.gateID
    
                current_path = []

                # Determine gate duo (= tuple)
                gate_duo = tuple(sorted([current_gateID, connected_gateID]))
                # print(f"Gate duo: {gate_duo}")

                # Do not continue if a path between the current and connected gate has already been made
                if gate_duo not in self.completed_connections:

                    # Get coordinates (= tuple: (x, y, z))
                    current_gate_coords = (current_gateObject.xcoord, current_gateObject.ycoord, current_gateObject.zcoord)
                    connected_gate_coords = (connected_gateObject.xcoord, connected_gateObject.ycoord, connected_gateObject.zcoord)

                    # print(f"Current gate coord: {current_gate_coords}")
                    # print(f"Connected gate coord: {connected_gate_coords}")

                    # Add start coordinates to the current path
                    current_path.append(current_gate_coords)

                    # Compute steps
                    # steps_x, steps_y = self.compute_steps(current_gate_coords, connected_gate_coords)

                    # Compute relative Manhattan distances
                    relative_dist_x, relative_dist_y = self.compute_rel_Manhattandist(current_gate_coords, connected_gate_coords)
                    
                    # Create path
                    current_path_coordinates = self.create_path(current_gate_coords, relative_dist_x, relative_dist_y, connected_gate_coords)
                    current_path.extend(current_path_coordinates)

                    # Append current path to the total path
                    self.total_path[gate_duo] = current_path

                    # Update the completed connections set
                    self.completed_connections.add(gate_duo)

                    # Visulalize chip on each path of the algorithm
                    print(f"gate duo: {gate_duo}")
                    visualisation = Chip_Visualization(self.graph.gates, self.total_path)
                    visualisation.run()
        
        print(f"total path: {self.total_path}")
        return self.total_path

                
