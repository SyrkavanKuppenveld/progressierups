import numpy as numpy
from collections import Counter
from scipy.spatial import distance

class Wire():

    def __init__(self, grid, gates, connections):
        """Initialize Wire object."""

        self.gates = gates
        self.grid = grid
        self.connections = connections
        self.total_path = self.wire_path()
        self.wire_units, self.all_coordinates = self.get_wire_details()
        self.length = self.compute_length()
        self.intersections = self.count_intersections()
        self.collisions = self.count_collisions()
        self.current_level = 1

    def generate_path(self):
        """Returns generated wire path."""

        current_path = set()

        # Iterate over connections in netlist
        for connection in self.connections:

            for i in range(self.connections[connection]):

                path = set()

                # Get gateID's
                a, b = connection, self.connections[connection][i]

                # Get gate coordinates
                a_x, a_y, a_z = self.gates[a].xcoord, self.gates[a].ycoord, 0
                b_x, b_y, a_z = self.gates[b].xcoord, self.gates[b].ycoord, 0

                # Compute steps en difference for x and y
                x_steps = abs(b_x - a_x)
                x_diff = b_x - a_x
                y_steps = abs(b_y - a_y)
                y_diff = b_y - a_y
                z_steps = 0
                z_diff = 0

                x_current = a_x
                y_current = a_y
                z_current = 0

                x_update = a_x
                y_update = a_y
                z_update = 0


                # Update and append step coordinates
                while x_current != b_x and y_current != b_y and z_current != 0:

                    # Create options going east, west, north, south
                    option_e_coords = (x_current + 1, y_current, z_current)
                    option_w_coords = (x_current - 1, y_current, z_current)
                    option_n_coords = (x_current, y_current + 1, z_current)
                    option_s_coords = (x_current, y_current - 1, z_current)

                    options_current_level = [option_e_coords, option_w_coords, option_n_coords, option_s_coords]

                    # Calculate possible collisions
                    for option in direction_options:
                        if (current_path, option) in wire_units: ## Mimoun: Werkt 'wire_units' al goed?
                            direction_options.pop(option)


                    # If one option
                    if len(direction_options) == 1:
                        optimal_direction = direction_options[1]
                    
                    # If multiple options left, calculate best option according to Manhatten distance
                    elif len(direction_options) > 1:
                        direction_lengths = {}
                        for option in direction_options:
                            direction_lengths[option] = distance.cityblock([option[0], option[1]], [b_x, b_y])
                        optimal_direction = 0
                        for option in direction_options:
                            if direction_lengths[option] < optimal_direction:
                                optimal_direction = option
                    
                    # If no options on this level
                    elif len(direction_options) == 0:
                        
                        # Create options for up and down
                        option_u_coords = (x_current, y_current, z_current + 1)
                        option_d_coords = (x_current, y_current, z_current - 1)

                        # If down is no option
                        if z_current == 0 or option_d_coords in wire_units:
                            
                            # If up is no option; no options left
                            if option_u_coords in wire_units:
                                return 'Wire got stuck'
                            
                            # Go up
                            optimal_direction = option_u_coords

                            ## Mimoun: wire_path of wire_units? collision of intersection?

                    # Generate new wire line
                    current_coords = (x_current, y_current)
                    x_update = optimal_direction(0)
                    y_update = optimal_direction(1)
                    step_coords = (x_update, a_y)

                    # Only add new wire line if no collision occurs
                    ## Mimoun: Waarom checken we hier ook nog 'current_coords'? Als het goed is zit die sowieso al in path toch?
                    #  Syr: is deze niet voor het checken van collisions? Want je checkt (vertrekpunt, aankomstpunt) en dat is een wire-unit-length...
                    # ...dus eignenlijk houden we hier dan al rekening met de hard constraint van de collisions
                    ## Mimoun: Maar als current_coords en step_coords in path staan, betekent dat nog niet dat er collision is, toch?
                #    if (current_coords, step_coords) not in path:
                #        path.add(step_coords)
                #        x_current = x_update

                    if b_x == x_update:
                        print('x = check')
                                # Update and append step coordinates
                    if b_y == y_update:
                        print('y = check')

                    if b_z == z_update:
                        print('z = check')


        return total_path 
    

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
