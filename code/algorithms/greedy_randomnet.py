from code.classes import Wire
from code.visualization.visualize import Chip_Visualization
import random

class Greedy_RandomNet():
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. 

    Random element
    --------------
    * The order of the connections are generated randomly.
    * If multiple neighbors have the same distance, the next position is generated
      randomly. 
    
    Greedy element
    --------------
    The next position will be the neighbor with the lowest Manhattan distance.
    """

    def __init__(self, graph):
        """
        Initializes the Random Greedy Net algorithm.
        
        Parameters
        ----------
        graph: a Graph object
                A Graph object representing the chip grid.
        """
        
        self.graph = graph
        self.wire = Wire()   

    def get_next_connection(self, connections):
        """Randomly returns a connection.
        
        Parameters
        ----------
        connections: a list
                A list containin the connections from the netlist file.

        Returns
        -------
        tuple
                Randomly generated tuple containing two gates that need to be connected.
        """

        return connections.pop(random.randrange(0, len(connections)))

    def next_position(self, position, goal):
        """
        Returns the next position, according to the lowest Manhattan Distance.
                
        Parameters
        ----------
        position: a Node object
                A Node object representing the current position of the wire.

        goal: a Node object
                A Node object repesenting the goal position on the grid.
        
        Returns
        -------
        Node object
                The Node object that will be the new position of the wire.
        """

        mdist = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                mdist.append((neighbor, dist))

        # tmp = position

        # Assign new position
        position = self.get_random_min(mdist)
        # print(tmp, position)
        # print(tmp.neighbors)
        # print(position in tmp.neighbors)

        return position

    def compute_manhattan_dist(self, position, goal):
        """
        Returns the Manhattan Distance between start and finish.
        
        Parameters
        ----------
        position: a Node object
                A Node object representing the current position of the wire.

        goal: a Node object
                A Node object repesenting the goal position on the grid.

        Returns
        -------
        int 
                The Manhattan Distance.
        """

        x_dist = abs(position.xcoord - goal.xcoord)
        y_dist = abs(position.ycoord - goal.ycoord)
        z_dist = abs(position.zcoord - goal.zcoord)

        return x_dist + y_dist + z_dist

    def get_random_min(self, lst):
        """
        Returns step with lowest Manhattan Distance, if multiple it returns one 
        randomly.

        Parameters
        ----------
        list: a list
                A list with tuples. First element of tuple is the neighbor and the 
                second element is the Manhattan distance. 

        Returns
        -------
        Node object
                The Node object with the minimal Manhattan Distance, if multiple with the
                Node object is randomly choosen.
        """
        
        # Get minimum Manhattan Distance of steps
        # print(f"list: {lst}")
        # print(f"min_value: {lst[1]}")
        min_value = min(lst, key=lambda x: x[1])

        # Create a list with all the steps with the minimum distance
        minimum = []
        for dist in lst:
            if dist[1] == min_value[1]:
                minimum.append(dist[0])

        return random.choice(minimum)

    def make_connection(self, gate_a, gate_b):
        """
        Returns set with wire path between gate_a and gate_b.
        
        Parameters
        ----------
        gate_a: int
                A integer representing the gateID of gate_a.

        gate_a: int
                A integer representing the gateID of gate_b.

        Returns
        -------
        tuple
                A tuple containing the wire path to connect gate_a and gate_b.
        """
        
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
            
            # Increment position.intersection if position is not a gate
            if position.isgate is False:
                position.increment_intersection()

            # Append step to wire path
            wire_path.append((position.xcoord, position.ycoord, position.zcoord))
        
        print(wire_path)
        
        return wire_path

    def run(self):
        """
        Returns a dictionary with the wire route to connect all gates according to netlist.

        Returns
        -------
        dict 
                A dictionary containing the route of the wire per connection.
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
            self.completed = len(route)

        #     # Visualize wire per connection
        #     visualization = Chip_Visualization(self.graph.gates, route)
        #     visualization.run()

        return route

