from code.classes import Wire
from code.visualization.visualize import Chip_Visualization
import random

class Greedy_RandomNet():
    """ Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. 
    
    The algorithm is random because the order in which the connections are made is
    randomly generated. Moreover, if multiple steps have the minimal distance, the
    next step is randomly generated. The algorithm is greedy, because it will 
    choose the gate with the lowest Manhattan distance. 
    """

    def __init__(self, graph):
        """Initializes the Random Greedy Net algorithm."""
        
        self.graph = graph
        self.wire = Wire()   

    def get_next_connection(self, connections):
        """Randomly returns a connection."""

        return connections.pop(random.randrange(0, len(connections)))

    def next_position(self, position, goal):
        """Returns the next position, according to the lowest Manhattan Distance."""

        mdist = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                mdist.append((neighbor, dist))
                  
        # Assign new position
        position = self.get_random_min(mdist)

        return position

    def compute_manhattan_dist(self, start, finish):
        """Returns the Manhattan Distance between start and finish."""

        x_dist = abs(start.xcoord - finish.xcoord)
        y_dist = abs(start.ycoord - finish.ycoord)
        z_dist = abs(start.zcoord - finish.zcoord)

        return x_dist + y_dist + z_dist

    def get_random_min(self, lst):
        """Returns step with lowest Manhattan Distance, if multiple it returns one 
        randomly.
        """
        
        # Get minimum Manhattan Distance of steps
        min_value = min(lst, key=lambda x: x[1])

        # Create a list with all the steps with the minimum distance
        minimum = []
        for dist in lst:
            if dist[1] == min_value[1]:
                minimum.append(dist[0])

        return random.choice(minimum)

    def make_connection(self, gate_a, gate_b):
        """Returns set with wire path between gate_a and gate_b."""
        
        wire_path = []

        # Get correspoding nodes for position(gate_a) and goal(gate_b)
        position = self.graph.nodes[(gate_a.xcoord, gate_a.ycoord, gate_a.zcoord)]
        goal = self.graph.nodes[(gate_b.xcoord, gate_b.ycoord, gate_b.zcoord)]

        # Add start position to wire path
        wire_path.append((position.xcoord, position.ycoord, position.zcoord))

        # Iterate until connection has been made
        while position != goal:
            
            # Store current position in temporary value
            tmp = position

            # Generate next position
            position = self.next_position(position, goal)

            # Update wire path and coordinates
            self.wire.update_path(tmp, position)
            self.wire.update_coords(position)

            # Append step to wire path
            wire_path.append((position.xcoord, position.ycoord, position.zcoord))
        
        return tuple(wire_path)
   
    def run(self):
        """Returns dict with the wire route to connect all gates according 
        to netlist.
        """

        route = {}
        netlist = list(self.graph.netlist)

        # Iterate until netlist is empyt
        while netlist:

            # Get random connection 
            connection = netlist.pop(random.randrange(0, len(netlist)))

            # Get corresponding Gate objects
            a, b = connection[0], connection[1]
            gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

            # Generate the connection between gate a and b
            route[(a, b)] = self.make_connection(gate_a, gate_b)

        return route

