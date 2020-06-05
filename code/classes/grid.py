
import numpy as np

class Grid():

    def __init__(self, gates):
        """Initialize Grid object."""

        self.gates = gates
        self.grid = self.create_grid(gates)
        self.filled_grid = self.fill_grid(self.gates, self.grid)
    
    def create_grid(self, gates):
        """"Returns empty grid."""

        x_values = []
        y_values = []

        # Get x and y coordinates per gate
        for gate in gates:
            x_values.append(gates[gate].xcoord)
            y_values.append(gates[gate].ycoord)

        # Get max grid coordinates 
        # 2 is for initialization of outer edges
        nx = max(x_values) + 2
        ny = max(y_values) + 2

        # Generate zero grid
        grid = np.zeros((ny, nx))

        return grid

    def fill_grid(self, gates, grid):
        """Returnes grid with gate coordinates."""
        
        # Fill gates in grid
        for gate in self.gates:
            x = gates[gate].xcoord
            y = 6 - gates[gate].ycoord
            grid[y][x] = gate
        
        return grid

        


