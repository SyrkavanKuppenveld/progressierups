import numpy as numpy

class Wire():

    def __init__(self, grid, gates, netlist):
        """Initialize Wire object."""

        self.gates = gates
        self.grid = grid
        self.netlist = netlist
        self.start_x = self.gates[1].xcoord
        self.start_y = self.gates[1].ycoord
        self.path = self.wire_path()

    def wire_path(self):

        path = []

        for connection in self.netlist:
            
            # Get gateID's
            a, b = connection[0], connection[1]

            # Get gate coordinates
            a_x, a_y = self.gates[a].xcoord, self.gates[a].ycoord
            b_x, b_y = self.gates[b].xcoord, self.gates[b].ycoord

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

        print(path)


        return path



'***************************************************************************'