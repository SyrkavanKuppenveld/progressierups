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
            
            print

            # Get gateID's
            a, b = connection[0], connection[1]

            # Get gate coordinates
            a_x, a_y = self.gates[a].xcoord, self.gates[a].ycoord
            b_x, b_y = self.gates[b].xcoord, self.gates[b].ycoord

            print(b_x, b_y)

            x_steps = b_x - a_x
            y_steps = b_y - a_y

            x_update = a_x

            if x_steps > 0:
                
                for _ in range(x_steps):
                    x_update += 1
                    step_coords = (x_update, a_y)
                    path.append(step_coords)

                    if b_x == x_update:
                        print('check')
            
            elif x_steps < 0:
                
                for _ in range(x_steps,):
                    x_update -= 1
                    step_coords = (x_update, a_y)
                    path.append(step_coords)

                    if b_x == x_update:
                        print('check')

            y_update = a_y

            if y_steps > 0:

                for _ in range(y_steps):
                    y_update += 1
                    step_coords = (x_update, y_update)
                    path.append(step_coords)

                    if b_y == y_update:
                        print('check')
            
            elif y_steps < 0:

                for _ in range(y_steps):
                    y_update -= 1
                    step_coords = (x_update, y_update)
                    path.append(step_coords)

                    if b_y == y_update:
                        print('check')



            # else:
            #     pass

        print(path)


        return 1



'***************************************************************************'