import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    ax.set_zlim(0,10)

    # Add gates to the 3D plot
    for gate in gates:
        xs = gates[gate].xcoord
        ys = gates[gate].ycoord
        zs = 0
        ax.scatter(xs, ys, zs, color='firebrick')

    # Add wire paths to the 3D plot
    for path in total_path:
        current_path = total_path[path]
        x_coords = []
        y_coords = []
        for coord in current_path:
            x_coords.append(coord[0])
            y_coords.append(coord[1])

        ax.plot(x_coords, y_coords, color='lightseagreen')
    
    plt.show()

