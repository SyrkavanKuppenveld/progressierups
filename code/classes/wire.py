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
        self.cost = self.length + (300 * self.intersections)


    def wire_path(self):
        """Returns wire path."""

        total_path = {}

        # Iterate over connections
        for connection in self.connections.graph:

            print(connection)

            for i in range(len(self.connections.graph[connection])):

                path = []
                
                # Get gateID's
                gate_a, gate_b = connection, self.connections.graph[connection][i]

                # Get gate coordinates
                gate_a_x, gate_a_y = self.gates[gate_a].xcoord, self.gates[gate_a].ycoord
                gate_b_x, gate_b_y = self.gates[gate_b].xcoord, self.gates[gate_b].ycoord

                start_coords = (gate_a_x, gate_a_y)
                path.append(start_coords)

                # Compute steps en difference for x and y
                x_steps = abs(gate_b_x - gate_a_x)
                x_diff = gate_b_x - gate_a_x
                y_steps = abs(gate_b_y - gate_a_y)
                y_diff = gate_b_y - gate_a_y

                x_update = gate_a_x

                # Approach if difference x > 0
                if x_diff > 0:
                    
                    # Update and append step coordinates
                    for step in range(x_steps):
                        x_update += 1
                        step_coords = (x_update, gate_a_y)
                        path.append(step_coords)

                        if gate_b_x == x_update:
                            print(f'x = check')
                
                # Approach if difference x < 0
                elif x_diff < 0:
                    
                    # Update and append step coordinates
                    for step in range(x_steps):
                        x_update -= 1
                        step_coords = (x_update, gate_a_y)
                        path.append(step_coords)

                        if gate_b_x == x_update:
                            print(f'x = check')

                elif x_diff == 0:
                    print(f'x = check')

                y_update = gate_a_y

                # Approach if difference y > 0
                if y_diff > 0:

                    # Update and append step coordinates
                    for step in range(y_steps):
                        y_update += 1
                        step_coords = (x_update, y_update)
                        path.append(step_coords)

                        if gate_b_y == y_update:
                            print(f'y = check')
                
                # Approach if difference y < 0
                elif y_diff < 0:

                    # Update and append step coordinates
                    for step in range(y_steps):
                        y_update -= 1
                        step_coords = (x_update, y_update)
                        path.append(step_coords)

                        if gate_b_y == y_update:
                            print(f'y = check')

                elif y_diff == 0:
                    print(f'y = check')
                
                # Create dict entry for path with connection as key
                # Ensure that every connection is added only once
                combination = sorted([gate_a, gate_b])
                combination = tuple(combination)
                total_path[combination] = path

        print('total path:')
        print(total_path)

        return total_path


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
                a_x, a_y = self.gates[a].xcoord, self.gates[a].ycoord
                b_x, b_y = self.gates[b].xcoord, self.gates[b].ycoord

                # Compute steps en difference for x and y
                x_steps = abs(b_x - a_x)
                x_diff = b_x - a_x
                y_steps = abs(b_y - a_y)
                y_diff = b_y - a_y

                x_current = a_x
                y_current = a_y

                x_update = a_x
                y_update = a_y


                # Update and append step coordinates
                while b_x != x_current and b_y != y_current:
                    
                    # Create options going east, west, north and south
                    option_e_coords = (b_x + 1, b_y)
                    option_w_coords = (b_x - 1, b_y)
                    option_n_coords = (b_x, b_y + 1)
                    option_s_coords = (b_x, b_y - 1)

                    direction_options = [option_e_coords, option_w_coords, option_n_coords, option_s_coords]

                    # Calculate possible collisions
                    # Syrka: Hier vind je geen collisions mee, want je checkt alleen coordinaten, dus je kan hier wel
                    # intersections mee checken maar voor een collision heb je een a-coordinaat (vertrekpunt) en een
                    # b-coordinaat nodig (aankomst punt). Als je deze dan gezamelijk (in een lijst van tuples bv) opslaat, 
                    # dan kun je collisions checken
                    for option in direction_options:
                        if option in path:
                            direction_options.pop(option)
                    
                    # If no options
                    if len(direction_options) == 0:
                        pass
                        ## Mimoun: Wat als er geen opties zijn?
                        # Syrka: Misschien een volledige restart of een stap terug waarbij je de huidige stap uitsluit als mogelijke optie?

                    # If one option
                    elif len(direction_options) == 1:
                        optimal_direction = direction_options[1]
                    
                    # If multiple options left, calculate closest option according to Manhatten distance
                    elif len(direction_options) > 1:
                        direction_lengths = {}
                        for option in direction_options:
                            direction_lengths[option] = distance.cityblock([option[0], option[1]], [b_x, b_y])
                        optimal_direction = 0
                        for option in direction_options:
                            if direction_lengths[option] < optimal_direction:
                                optimal_direction = option


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
    
        print(collisions)

        return collisions

    def compute_cost(self):
        """ Returns the cost of the wire."""

        intersections = self.count_intersections()
        cost = self.length + (300 * intersections)
        
        return cost


    

            


'***************************************************************************'