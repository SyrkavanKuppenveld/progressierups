import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visualise_chip(gates, wire_path):
    """ Visualises the chip Object in 3D."""

    gates = gates
    total_path = wire_path

    # Create 3D plot
    fig = plt.figure()  
    ax = fig.add_subplot(111, projection='3d') 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim(0,7)

    # Add gates to the 3D plot
    for gate in gates:
        xs = gates[gate].xcoord
        ys = gates[gate].ycoord
        zs = 0
        ax.scatter(xs, ys, zs, color='firebrick')

    # Add wire paths to the 3D plot
    x_max_chip = 0
    y_max_chip = 0
    
    for path in total_path:
        current_path = total_path[path]
        x_coords = []
        y_coords = []

        for coord in current_path:
            x_coords.append(coord[0])
            y_coords.append(coord[1])

        ax.plot(x_coords, y_coords, color='lightseagreen')

        # Store maxima of the x- and y- dimensions for later use
        x_max_path = max(x_coords)
        y_max_path = max(x_coords)

        if x_max_path > x_max_chip:
            x_max_chip = x_max_path 

        if y_max_path > y_max_chip:
            y_max_chip = y_max_path 

    # Visualise chip layers
    x_layer = np.linspace(0, x_max_chip, num=50)
    y_layer = np.linspace(0, y_max_chip, num=50)
    X, Y= np.meshgrid(x_layer, y_layer)

    # Create 3D plane for each layer
    for i in range(6):   
        Z = np.power(X, 0) * (i + 1)
        ax.plot_surface(X, Y, Z, color='lightcyan', alpha=0.5)
    
    plt.show()

