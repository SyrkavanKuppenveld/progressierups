import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.classes.gates import Gate
# from code.classes.grid import Grid
from code.classes.wire import Wire
from code.classes.graph import Graph

class Chip():
    def __init__(self, gates, connections):
        """Initialize Chip object."""

        self.gates = gates
        self.connections = connections
        # self.grid = self.get_grid()
        self.wire = self.construct_wirePath()

    # def get_grid(self):
    #     """Returns chip grid with gates filled in."""

    #     grid = Grid(self.gates)
        
        # return grid.grid

    def construct_wirePath(self):
        """Returns constructed wire path."""
         
        wire = Wire(self.gates, self.connections)

        return wire.total_path




 

  



