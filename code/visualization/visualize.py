import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mtick
import numpy as np

import pandas as pd
from pandas import DataFrame


class ChipVisualization():
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
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))

        self.fig = fig
        self.ax = ax

    def plot_gates(self):
        """ Adds gates to the 3D plot."""

        x_coord_gates = []
        y_coord_gates = []

        # Get coordinates of the gates
        for gate in self.gates:
            x = self.gates[gate].xcoord
            y = self.gates[gate].ycoord
            z = self.gates[gate].zcoord
            
            # Plot gate
            self.ax.scatter(x, y, z, color='firebrick')

            # Store the x- and y- coordinates of the gates
            x_coord_gates.append(x)
            y_coord_gates.append(y)

        # Retrieve maximum x- and y- coordinates of the gates
        x_max_gate = max(x_coord_gates)
        y_max_gate = max(y_coord_gates)

        # Adjust chip oulines
        self.ax.set_xlim(0,x_max_gate + 1)
        self.ax.set_ylim(0,y_max_gate + 1)

    def plot_wire(self):
        """ Adds wire paths to the 3D plot."""
        
        colors = ['lightseagreen', 'darkgray', 'lightcoral', 'gold'
                    , 'yellowgreen', 'salmon', 'dimgray', 'turquoise'
                    , 'coral', 'powderblue', 'navajowhite', 'teal', 'mediumseagreen'
                    , 'crimson', 'goldenrod', 'steelblue', 'pink', 'palegreen'
                    , 'paleturquoise', 'plum', 'skyblue']
                    
        # Get path coords for each net in total_path
        for i, path in enumerate(self.total_path):
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
            self.ax.plot(x_coords, y_coords, z_coords, color=colors[i % 21])

    def visualise_layer(self):
        """ Adds chip layers to the 3D plot."""

        x_layer = np.linspace(0, self.x_max_chip, num=5)
        y_layer = np.linspace(0, self.y_max_chip, num=5)
        X, Y = np.meshgrid(x_layer, y_layer)

        # Create 3D plane to represent each layer
        for i in range(7):   
            Z = np.power(X, 0) * (i + 1)
            self.ax.plot_surface(X, Y, Z, color='lightcyan', alpha=0.3)

    def run(self):
        """ Creates and displays the 3D visualisation of the chip."""
        
        # Initialize 3D plot
        self.create_3D_chip_outlines()
        
        # Add wire to plot
        self.plot_wire()

        # Add gates to plot
        self.plot_gates()

        # Visualise the layers of the chip
        self.visualise_layer()
        
        # Plot grid lines
        plt.grid(True)

        # Show the 3D visualisattion of the Chip
        plt.show()


class wireHeatmap(ChipVisualization):
    """ Visualise 3D wire density of the given solution."""    

    def __init__(self, nodes, wireObject):
        """
        Initializes components of the heatmap

        Parameters
        ----------
        nodes : dict
                A dictionary containting all the Nodes (coordinates) of the Graph (Chip)
        wireObject : a Wire Object
                A Wire Object which is a solution of an algorithm
        """

        self.nodes = nodes
        self.wire = wireObject
        self.fig = None
        self.ax = None
    
    def get_data_frame(self):

        wireDensitiesList = []

        for coordinates in self.nodes:
            node = self.nodes[coordinates]
            wireDensity = node.get_wire_density(node, self.wire.path)
            wireDensitiesList.append([node.xcoord, node.ycoord, node.zcoord, wireDensity])

        return pd.DataFrame(wireDensitiesList, columns=['x','y','z', 'wire density'])    
        
    def plot_heat(self, DataFrame):

        self.ax.scatter(DataFrame[['x']], DataFrame[['y']], DataFrame[['z']], marker='s', s=140, c=DataFrame[['wire density']], cmap='Reds', alpha=0.5)

    def run(self):
        """ Creates and displays the 3D wire density of the solution."""

        # Initialize 3D plot
        self.create_3D_chip_outlines()

        # Create DataFrame of data that is to be used
        dfNodeWireDensities = self.getDataFrame()

        # Plot wire density per node
        self.plot_heat(dfNodeWireDensities)

        # Show the 3D visualisattion of the wire density
        plt.show()