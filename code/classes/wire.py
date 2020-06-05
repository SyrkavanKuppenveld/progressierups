import numpy as numpy
from collections import Counter

class Wire():

    def __init__(self, grid, gates, netlist):
        """Initialize Wire object."""

        self.gates = gates
        self.grid = grid
        self.netlist = netlist
        self.start_x = self.gates[1].xcoord
        self.start_y = self.gates[1].ycoord
        self.total_path = self.wire_path()
        self.wire_units, self.all_coordinates = self.get_wire_details()
        self.length = self.compute_length()
        self.intersections = self.count_intersections()
        self.collisions = self.count_collisions()

    def wire_path(self):

        total_path = {}

        for connection in self.netlist:

            path = []
            
            # Get gateID's
            a, b = connection[0], connection[1]

            # Get gate coordinates
            a_x, a_y = self.gates[a].xcoord, self.gates[a].ycoord
            b_x, b_y = self.gates[b].xcoord, self.gates[b].ycoord

            start_coords = (a_x, a_y)
            path.append(start_coords)

            # Compute steps en difference for x and y
            x_steps = abs(b_x - a_x)
            x_diff = b_x - a_x
            y_steps = abs(b_y - a_y)
            y_diff = b_y - a_y

            x_update = a_x

            # Approach if difference x > 0
            if x_diff > 0:
                
                # Update and append step coordinates
                for _ in range(x_steps):
                    x_update += 1
                    step_coords = (x_update, a_y)
                    path.append(step_coords)

                    if b_x == x_update:
                        print(f'x = check')
            
            # Approach if difference x < 0
            elif x_diff < 0:
                
                # Update and append step coordinates
                for _ in range(x_steps):
                    x_update -= 1
                    step_coords = (x_update, a_y)
                    path.append(step_coords)

                    if b_x == x_update:
                        print(f'x = check')

            elif x_diff == 0:
                print(f'x = check')

            y_update = a_y

            # Approach if difference y > 0
            if y_diff > 0:

                # Update and append step coordinates
                for _ in range(y_steps):
                    y_update += 1
                    step_coords = (x_update, y_update)
                    path.append(step_coords)

                    if b_y == y_update:
                        print(f'y = check')
            
            # Approach if difference y < 0
            elif y_diff < 0:

                # Update and append step coordinates
                for _ in range(y_steps):
                    y_update -= 1
                    step_coords = (x_update, y_update)
                    path.append(step_coords)

                    if b_y == y_update:
                        print(f'y = check')

            elif y_diff == 0:
                print(f'y = check')
            
            # Create dict entry for path with connection as key
            total_path[connection] = path


        print(total_path)


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

                # Get wire-unit when two coordinates are present in the storage
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
    
        return collisions


    

            


'***************************************************************************'