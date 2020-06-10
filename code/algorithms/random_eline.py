import numpy as numpy
from collections import Counter
from scipy.spatial import distance

class RandomEline():

    def __init__(self, connections, gates):

        self.connections = connections
        self.gates = gates

    def run(self):
        """Returns wire path."""

        total_path = {}

        # Iterate over connections
        for gate in self.connections:

            for connection in self.connections[gate]:

                path = []
                
                # Get gateID's
                gate_a, gate_b = gate, connection

                # Get gate coordinates
                gate_a_x, gate_a_y = gate_a.xcoord, gate_a.ycoord
                gate_b_x, gate_b_y = gate_b.xcoord, gate_b.ycoord

                # print(f'gateax = {gate_a_x}')

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
                    for _ in range(x_steps):
                        x_update += 1
                        step_coords = (x_update, gate_a_y)
                        path.append(step_coords)

                        if gate_b_x == x_update:
                            print(f'x = check')
                
                # Approach if difference x < 0
                elif x_diff < 0:
                    
                    # Update and append step coordinates
                    for _ in range(x_steps):
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
                    for _ in range(y_steps):
                        y_update += 1
                        step_coords = (x_update, y_update)
                        path.append(step_coords)

                        if gate_b_y == y_update:
                            print(f'y = check')
                
                # Approach if difference y < 0
                elif y_diff < 0:

                    # Update and append step coordinates
                    for _ in range(y_steps):
                        y_update -= 1
                        step_coords = (x_update, y_update)
                        path.append(step_coords)

                        if gate_b_y == y_update:
                            print(f'y = check')

                elif y_diff == 0:
                    print(f'y = check')
                
                # Create dict entry for path with connection as key
                # Ensure that every connection is added only once
                combination = sorted([gate_a.gateID, gate_b.gateID])
                combination = tuple(combination)
                total_path[combination] = path

        print('total path:')
        print(total_path)

        return total_path