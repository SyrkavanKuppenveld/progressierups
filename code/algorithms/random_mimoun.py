import numpy as numpy
from collections import Counter
from scipy.spatial import distance
import random

class RandomGreedy():

    def __init__(self, grid, gates, connections):
        """Initialize Wire object."""

        self.gates = gates
        self.grid = grid
        self.connections = connections
        self.wire_units = {}
        self.wire_path = []
        self.length = self.compute_length()
        self.intersections = self.count_intersections()
        self.collisions = self.count_collisions()
        self.current_level = 1
        self.all_coordinates = []

    def run(self):
        """Returns generated wire path."""

        # Iterate over connections in netlist
        for connection in self.connections:

            for i in range(self.connections[connection]):

                path = set()

                # Get gateID's
                a, b = connection, self.connections[connection][i]

                # Get gate coordinates
                a_x, a_y, a_z = self.gates[a].xcoord, self.gates[a].ycoord, 0
                b_x, b_y, b_z = self.gates[b].xcoord, self.gates[b].ycoord, 0

                # Initialize wire coordinates
                x_current = a_x
                y_current = a_y
                z_current = 0
                current_location = [x_current, y_current, z_current]

                x_update = a_x
                y_update = a_y
                z_update = 0


                # While Gate b not yet reached
                while x_current != b_x and y_current != b_y and z_current != 0:
                    
                    # Add current wire unit to path
                    current_location = [x_current, y_current, z_current]
                    self.wire_path.append(current_location)
                    
                    # Try current level first
                    # Create options going east, west, north, south
                    option_e_coords = (x_current + 1, y_current, z_current)
                    option_w_coords = (x_current - 1, y_current, z_current)
                    option_n_coords = (x_current, y_current + 1, z_current)
                    option_s_coords = (x_current, y_current - 1, z_current)

                    options_current_level = [option_e_coords, option_w_coords, option_n_coords, option_s_coords]

                    # Calculate possible collisions
                    for option in options_current_level:
                        if (current_location, option) in self.wire_units or (option, current_location) in self.wire_units:
                            options_current_level.pop(option)

                    # If one option
                    if len(options_current_level) == 1:
                        optimal_direction = options_current_level[0]

                    # If multiple options left, calculate best option according to Manhatten distance
                    elif len(options_current_level) > 1:
                        direction_lengths = {}
                        for option in options_current_level:
                            direction_lengths[option] = distance.cityblock([option[0], option[1]], [b_x, b_y, b_z])
                        
                        # Get option with lowest Manhattan distance
                        shortest_distance = min(direction_lengths, key=direction_lengths.get)
                        if len(shortest_distance) == 1:
                            optimal_direction = shortest_distance[0]
                        else:
                            optimal_direction = random.choice(shortest_distance)

                    # If no options on current level
                    elif len(options_current_level) == 0:
                        
                        # Create options for up and down
                        option_u_coords = (x_current, y_current, z_current + 1)
                        option_d_coords = (x_current, y_current, z_current - 1)

                        # If down is no option
                        if z_current == 0 or (current_location, option_d_coords) in wire_units or (option_d_coords, current_location) in wire_units:
                            
                            # If up is no option; no options left
                            if (current_location, option_u_coords) in wire_units or (option_u_coords, current_location) in wire_units:
                                return f'Wire got stuck at {current_location}'
                            
                            # Go up
                            optimal_direction = option_u_coords


                    # Generate new wire line
                    x_update = optimal_direction(0)
                    y_update = optimal_direction(1)
                    z_update = optimal_direction(2)
                    next_location = (x_update, y_update, z_update)

                    # Add new wire path
                    self.wire_units.add((current_location, next_location))
                    path.add(next_location)

                    if b_x == x_update:
                        print('x = check')
                                # Update and append step coordinates
                    if b_y == y_update:
                        print('y = check')

                    if b_z == z_update:
                        print('z = check')

        return self.wire_path
    

    def get_wire_details(self):

        all_coordinates = []
        wire_units = []

        for gate in self.total_path:
            # Stores a maximum of two coordinates
            temp_storage = []

            path_coordinates = self.total_path[gate]

            for coordinate in path_coordinates:
                all_coordinates.append(coordinate)
                temp_storage.append(coordinate)

                # Get wire-unit coordinates when two coordinates are present in the storage
                if len(temp_storage) == 2:
                    wire_units.append((temp_storage[0], temp_storage[1]))
                    
                    # Discard first coord to make room for next coord of path
                    temp_storage.pop(0)
            
        return wire_units, all_coordinates

    def compute_length(self):
        """ Returns wire length."""

        return len(self.wire_units)

    def count_intersections(self):
        """ Returns the number of intersections."""

        path_coordinates = []
        intersections = 0

        # Find every coordinate in path
        for wire_piece in self.wire_path:
            for coordinates in wire_piece:
                if coordinates in path_coordinates:
                    intersections += 1
                path_coordinates.append(coordinates)

        for coordinate in unique_coordinates:
            if 
        

        # Counts occurences of coordinates
        coordinate_counter = Counter(self.all_coordinates)
        coordinates_sum = sum(coordinate_counter.values())

        # Counts uniquely visited coordinates
        unique_coordinates = len(coordinate_counter)

        # Subtracts the number of unique coordinates since an intersection 
        # starts when a coordinate is >1 times present
        intersections = coordinates_sum - unique_coordinates

        return intersections

    def count_collisions(self):
        """ Returns the number of collisions."""

        # Sorts wire units since to ensure that a wire unit from
        # A > B is equal to B > A
        sorted_wir_units = sorted(self.wire_units)
        
        # Counts occurences of wire units
        collisions_counter = Counter(sorted_wir_units)
        collisions_sum = sum(collisions_counter.values())
        
        # Counts uniquely visited wire units
        unique_wire_units = len(collisions_counter)

        # Subtracts the number of unique wire units since a collision 
        # starts when a wire unit is >1 times present
        collisions = collisions_sum - unique_wire_units

        print(collisions)

    def cost(self):
        """ Returns the current cost."""

        length = self.length
        intersections = self.intersections
        cost = length + (300 * intersections)

        return cost


    

            


'***************************************************************************'
