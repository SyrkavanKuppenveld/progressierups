import numpy as np

class Grid():

    def __init__(self, gates):
        """Initialize Grid object."""

        self.gates = gates
        self.grid = self.create_grid()
    
    def create_grid(self):
        """"Returns empty grid."""


        x_values = []
        y_values = []

        # Get x and y coordinates per gate
        for gate in self.gates:
            print(gate)
            print(self.gates)
            x_values.append(self.gates[gate].xcoord)
            y_values.append(self.gates[gate].ycoord)

        # Get gid initialization values for x and y
        # 2 is for addition outer edges
        nx = max(x_values) + 2
        ny = max(y_values) + 2

        # Generate zero grid
        grid = np.zeros((ny, nx))

        return grid

        


