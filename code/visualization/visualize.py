import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Chip_Visualization():
    """ Provides a visualisation of the Chip Object in 3D."""
    
    def __init__(self, gates, wire_path):
        """
        Initializes the components of the chip

        Parameters
        ----------
        gates : a list
            A list of gate coordinates (x, y, z)
        wire_path : a dict 
                A dictionary (key = net) of paths between the gates (value: list of coordinates)
        """

        self.gates = gates
        self.total_path = wire_path
        self.fig = None
        self.ax = None
        self.x_max_chip = 0
        self.y_max_chip = 0


    def create_3D_chip_outlines(self):
        """ Creates a 3D figure."""
        
        fig = plt.figure()  
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_zlim(0,7)

        self.fig = fig
        self.ax = ax

    def plot_gates(self):
        """ Adds gates to the 3D plot."""

        # Get coordinates of the gates
        for gate in self.gates:
            xs = self.gates[gate].xcoord
            ys = self.gates[gate].ycoord
            zs = self.gates[gate].zcoord
            
            # Plot gate
            self.ax.scatter(xs, ys, zs, color='firebrick')

    def plot_wire(self):
        """ Adds wire paths to the 3D plot."""
        
        # Get path coords for each net in total_path
        for path in self.total_path:
            current_path = self.total_path[path]
            x_coords = []
            y_coords = []
            z_coords = []

            # Get wire coordinates
            for coord in current_path:
                x_coords.append(coord[0])
                y_coords.append(coord[1])
                z_coords.append(coord[2])

            # Plot net-path
            self.ax.plot(x_coords, y_coords, z_coords, color='lightseagreen')

            # Store maxima of the x- and y- dimensions for later use
            if x_coords:
                x_max_path = max(x_coords)
            if y_coords:
                y_max_path = max(x_coords)

            if x_max_path > self.x_max_chip:
                self.x_max_chip = x_max_path 
            if y_max_path > self.y_max_chip:
                self.y_max_chip = y_max_path 

    def visualise_layer(self):
        """ Adds chip layers to the 3D plot."""

        x_layer = np.linspace(0, self.x_max_chip, num=50)
        y_layer = np.linspace(0, self.y_max_chip, num=50)
        X, Y = np.meshgrid(x_layer, y_layer)

        # Create 3D plane to represent each layer
        for i in range(7):   
            Z = np.power(X, 0) * (i + 1)
            self.ax.plot_surface(X, Y, Z, color='lightcyan', alpha=0.5)

    def run(self):
        """ Creates and displays the 3D visualisation of the chip."""
        
        # Initialize 3D plot
        self.create_3D_chip_outlines()
        
        # Add gates to plot
        self.plot_gates()

        # Add wire to plot
        self.plot_wire()

        # Visualise the layers of the chip
        self.visualise_layer()
        
        # Aan te passen opmaak raster/ticks
        
        # Show no axes at all
        # plt.axis('off')

        # Hide the axes altogether
        # self.ax.axes.xaxis.set_ticks([])
        # self.ax.axes.yaxis.set_ticks([])
        # self.ax.axes.zaxis.set_ticks([])

        # Hide the numbers on the axes
        # self.ax.axes.xaxis.set_ticklabels([])
        # self.ax.axes.yaxis.set_ticklabels([])
        # self.ax.axes.zaxis.set_ticklabels([])

        # Plot grid lines
        plt.grid(True)

        # Show the 3D visualisattion of the Chip
        plt.show()

