import numpy as numpy
from collections import Counter
from scipy.spatial import distance
from code.algorithms import RandomEline

class Wire():

    def __init__(self, gates, connections):
        """Initialize Wire object."""

        self.gates = gates
        self.connections = connections
        self.algorithm = RandomEline(connections, gates)
        self.total_path = self.algorithm.run()
        self.wire_units, self.all_coordinates = self.get_wire_details()
        
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

                # Get wire-unit coordinates: when two coordinates are present in the storage, create wire length unit
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

        # Sorts wire units  to ensure that a wire unit from
        # A > B is equal to B > A
        sorted_wir_units = sorted(self.wire_units)
        
        # Counts occurences of wire units
        collisions_counter = Counter(sorted_wir_units)
        collisions_sum = sum(collisions_counter.values())
        
        # Counts unique visited wire units
        unique_wire_units = len(collisions_counter)
        
        # Subtracts the number of unique wire units since a collision 
        # starts when a wire unit is >1 times visited
        collisions = collisions_sum - unique_wire_units
    
        print(f'collisions')
        print(collisions)

        return collisions

    def compute_cost(self):
        """ Returns the cost of the wire."""

        intersections = self.count_intersections()
        cost = self.length + (300 * intersections)
        
        return cost


    

            


'***************************************************************************'