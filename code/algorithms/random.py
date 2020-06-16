import random
from code.classes.wire import Wire
from code.visualization.visualize import Chip_Visualization

class Random():
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
                A list containing the connections from the netlist file.

        Returns
        -------
        tuple
                Randomly generated tuple containing two gates that need to be connected.
        """

        return connections.pop(random.randrange(0, len(connections)))

    def get_next_neighbor(self, neighbors):
        """Randomly returns a neighbor.
        
        Parameters
        ----------
        connections: a list
                A list containing the neighbors of the current position of the wire.

        Returns
        -------
        Node object
                Randomly generated neighbor Node.
        """

        return neighbors.pop(random.randrange(0, len(neighbors)))

    def next_position(self, position, goal):
        """
        Returns the next position, according to the lowest Manhattan Distance.
                
        Parameters
        ----------
        position: a Node object
                A Node object representing the current position of the wire.

        goal: a Node object
                A Node object representing the goal position.
        
        Returns
        -------
        Node object
                The Node object that will be the new position of the wire.
        """

        neighbors = list(position.neighbors)

        while neighbors:
            neighbor = self.get_next_neighbor(neighbors)
            if self.wire.check_collision(position, neighbor):
                return neighbor

        raise ValueError

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

            # Append step to wire path
            wire_path.append((position.xcoord, position.ycoord, position.zcoord))
        
        return tuple(wire_path)
   
    def run(self):
        """
        Returns dict with the wire route to connect all gates according to netlist.

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

        return route

