import numpy as numpy
from collections import Counter
import random
import copy
from code.classes.node import Node
from code.classes import Wire
from code.visualization.visualize import Chip_Visualization

class RandomGreedy():

    def __init__(self, graph):
        """Initialize Wire object."""

        self.graph = graph
        self.wire = Wire()

    def get_next_gate(self, gates):
        """Gets next gate and removes it from the list."""

        next_gate = gates.pop(0)

        return next_gate

    def get_next_connection(self, connections):
        """ Gets next connection and removes it from the list."""
        
        return connections.pop(0)

    def compute_manhattan_dist(self, start, finish):
        """Returns the Manhattan Distance between start and finish."""

        x_dist = abs(start.xcoord - finish.xcoord)
        y_dist = abs(start.ycoord - finish.ycoord)
        z_dist = abs(start.zcoord - finish.zcoord)

        return x_dist + y_dist + z_dist

    def next_position(self, position, goal):
        """Returns the next position."""

        mdist = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                mdist.append((neighbor, dist))
                    
        # Assign new position
        position = self.get_random_min(mdist)

        return position

    def get_random_min(self, lst):
        """Returns random minimum."""

        min_value = min(lst, key=lambda x: x[1])
        minimum = []
        for dist in lst:
            if dist == min_value:
                minimum.append(dist[0])

        return random.choice(minimum)

    def make_connection(self, gate_a, gate_b):
        """Returns wire connection between gate_a and gate_b."""

        connection = []

        # Get position and goal nodes
        position = self.graph.nodes[(gate_a.xcoord, gate_a.ycoord, gate_a.zcoord)]
        goal = self.graph.nodes[(gate_b.xcoord, gate_b.ycoord, gate_b.zcoord)]

        # Add position
        connection.append((position.xcoord, position.ycoord, position.zcoord))

        # Iterate until connection has been made
        while position != goal:
            
            # Store current position in temporary value
            tmp = position

            # Get next posotion
            position = self.next_position(position, goal)

            # Update wire path and coordinates
            self.wire.update_path(tmp, position)
            self.wire.update_coords(position)

            # Append connection
            connection.append((position.xcoord, position.ycoord, position.zcoord))
        
        return tuple(connection)

    def run(self):
        """Returns generated wire path."""

        route = {}
        netlist = list(self.graph.netlist)

        while netlist:

            # Get random connection 
            connection = netlist.pop(0)

            # Get corresponding Gate objects
            a, b = connection[0], connection[1]
            gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

            # Generate the connection between gate a and b
            route[(a, b)] = self.make_connection(gate_a, gate_b)

        return route

        # # Iterate over connections in netlist
        # for connection in self.connections:

        #     for i in range(self.connections[connection]):

        #         path = set()

        #         # Get gateID's
        #         a, b = connection, self.connections[connection][i]

        #         # Get gate coordinates
        #         a_x, a_y, a_z = self.gates[a].xcoord, self.gates[a].ycoord, 0
        #         b_x, b_y, b_z = self.gates[b].xcoord, self.gates[b].ycoord, 0

        #         # Initialize wire coordinates
        #         x_current = a_x
        #         y_current = a_y
        #         z_current = 0
        #         current_location = [x_current, y_current, z_current]

        #         x_update = a_x
        #         y_update = a_y
        #         z_update = 0


        #         # While Gate b not yet reached
        #         while x_current != b_x and y_current != b_y and z_current != 0:

        #             # Add current wire unit to path
        #             current_location = [x_current, y_current, z_current]
        #             self.wire_path.append(current_location)

        #             # Try current level first
        #             # Create options going east, west, north, south
        #             option_e_coords = (x_current + 1, y_current, z_current)
        #             option_w_coords = (x_current - 1, y_current, z_current)
        #             option_n_coords = (x_current, y_current + 1, z_current)
        #             option_s_coords = (x_current, y_current - 1, z_current)

        #             options_current_level = [option_e_coords, option_w_coords, option_n_coords, option_s_coords]

        #             # Calculate possible collisions
        #             for option in options_current_level:
        #                 if self.check_collision(current_location, option):
        #                     options_current_level.pop(option)

        #             # Calculate intersections
        #             for option in options_current_level:
        #                 if 

        #             # If one option
        #             if len(options_current_level) == 1:
        #                 optimal_direction = options_current_level[0]

        #             # If multiple options left, calculate best option according to Manhatten distance
        #             elif len(options_current_level) > 1:
        #                 direction_lengths = {}
        #                 for option in options_current_level:
        #                     direction_lengths[option] = distance.cityblock([option[0], option[1]], [b_x, b_y, b_z])

        #                 # Get option with lowest Manhattan distance
        #                 shortest_distance = min(direction_lengths, key=direction_lengths.get)
        #                 if len(shortest_distance) == 1:
        #                     optimal_direction = shortest_distance[0]
        #                 else:
        #                     optimal_direction = random.choice(shortest_distance)


        #             # If no options on current level
        #             elif len(options_current_level) == 0:
                        
        #                 # Create options for up and down
        #                 option_u_coords = (x_current, y_current, z_current + 1)
        #                 option_d_coords = (x_current, y_current, z_current - 1)

        #                 # If down is no option
        #                 if z_current == 0 or (current_location, option_d_coords) in wire_units or (option_d_coords, current_location) in wire_units:
                            
        #                     # If up is no option; no options left
        #                     if (current_location, option_u_coords) in wire_units or (option_u_coords, current_location) in wire_units:
        #                         return f'Wire got stuck at {current_location}'
                            
        #                     # Go up
        #                     optimal_direction = option_u_coords


        #             # Generate new wire line
        #             x_update = optimal_direction(0)
        #             y_update = optimal_direction(1)
        #             z_update = optimal_direction(2)
        #             next_location = (x_update, y_update, z_update)

        #             # Add new wire path
        #             self.wire_units.add((current_location, next_location))
        #             path.add(next_location)

        #             if b_x == x_update:
        #                 print('x = check')
        #                         # Update and append step coordinates
        #             if b_y == y_update:
        #                 print('y = check')

        #             if b_z == z_update:
        #                 print('z = check')

        # return self.wire_path


    def check_collision(self, current_location, coordinates):
        """ Returns True if coordinates result in collision. """

        if (current_location, coordinates) in self.wire_units or (coordinates, current_location) in self.wire_units:
            return True

        return False

    def check_intersection(self, coordinates):
        """ Returns True if coordinates result in intersection. """

        if coordinates in self.wire_path:
            return True

        return False


'***************************************************************************'
