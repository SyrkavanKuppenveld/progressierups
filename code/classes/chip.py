import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.classes.gates import Gate
# from code.classes.grid import Grid
from code.classes.wire import Wire
from code.classes.graph import Graph

class Chip():
    def __init__(self, gates, connections, layers):
        """Initialize Chip object."""

        self.gates = gates
        self.connections = connections
        # self.grid = self.get_grid()
        self.xcoord, self.ycoord = self.grid_coords()
        self.zcoord = layers
        self.wire = self.construct_wirePath()

    def grid_coords(self):
        """Returns the max x and y coordinates of the grid."""

        x = []
        y = []

        # Iterate over the gates
        for gate in self.gates:

            # Append x and y coordinates 
            xcoord = self.gates[gate].xcoord
            x.append(xcoord)
            ycoord = self.gates[gate].ycoord
            y.append(ycoord)

        # Get max x and y coordinates
        x_max, y_max = max(x), max(y)

        return x_max, y_max

    def construct_wirePath(self):
        """Returns constructed wire path."""
         
        wire = Wire(self.gates, self.connections)

        return wire.total_path




 

  



