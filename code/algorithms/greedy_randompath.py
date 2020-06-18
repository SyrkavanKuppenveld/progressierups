import random

from code.classes.wire import Wire
from code.visualization.visualize import Chip_Visualization

class Greedy_RandomPath():
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. 

    Random element
    --------------
    * If multiple neighbors have the same distance, the next position is selected
      randomly among those.
    
    Greedy element
    --------------
    The next position will be the neighbor with the lowest Manhattan distance from the target.
    """

    def __init__(self, graph):
        """
        Initializes the Random Greedy Path algorithm.
        
        Parameters
        ----------
        graph: a Graph object
                A Graph object representing the chip grid.
        """
        

        self.graph = graph
        self.wire = Wire()

    def get_next_gate(self, gates):
        """Gets next gate and removes it from the list.
        
        Parameters
        ----------
        gates: a list
                A list containing all gates for current netlist.
        
        Returns
        -------
        Gate object
                Returns next gate.
        
        """

        next_gate = gates.pop(0)

        # Ensure that next_gate has connections
        while next_gate not in self.graph.connections:
            next_gate = gates.pop(0)

        return next_gate

    def get_next_connection(self, connections):
        """Randomly returns a connection.

        Parameters
        ----------
        connections: a list
                A list containin the connections from the netlist file.

        Returns
        -------
        tuple
                Returns tuple containing the next two gates that need to be connected.
        """
        
        return connections.pop()

    def compute_manhattan_dist(self, start, finish):
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

        x_dist = abs(start.xcoord - finish.xcoord)
        y_dist = abs(start.ycoord - finish.ycoord)
        z_dist = abs(start.zcoord - finish.zcoord)

        return x_dist + y_dist + z_dist

    def next_position(self, position, goal):
        """
        Returns next position, preferring those without intersection.

        Parameters
        ----------
        position: a Node object
                A Node object representing the current position of the wire.

        goal: a Node object
                A Node object representing the goal position on the grid.
        
        Returns
        -------
        Node object
                The Node object that will be the new position of the wire.
        String
                Returns 'Stuck; no solution found' if no next step could be found.
        """

        # Store neighbors that do and don't result in intersections
        mdist = []
        mdist_intersection = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                if neighbor.intersection == 0:
                    mdist.append((neighbor, dist))
                else:
                    mdist_intersection.append((neighbor, dist))

        if len(mdist) == 0:
            mdist = mdist_intersection
                    
        # Assign new position
        try:
            position = self.get_random_min(mdist)
        except ValueError:
            return 'Stuck; no solution found'

        return position

    def get_random_min(self, lst):
        """
        Returns step with lowest Manhattan Distance, if multiple it returns one 
        randomly.

        Parameters
        ----------
        lst: a list
                A list with tuples. First element of tuple is the neighbor and the 
                second element is the Manhattan distance. 

        Returns
        -------
        Node object
                The Node object with the minimal Manhattan Distance from the goal gate. 
                If multiple, Node object is chosen randomly among those.
        """

        min_value = min(lst, key=lambda x: x[1])
        minimum = []
        for dist in lst:
            if dist == min_value:
                minimum.append(dist[0])

        return random.choice(minimum)

    def make_connection(self, gate_a, gate_b):
        """
        Returns set with wire path between gate_a and gate_b.

        Parameters
        ----------
        gate_a: int
                An integer representing the gateID of gate_a.

        gate_a: int
                An integer representing the gateID of gate_b.

        Returns
        -------
        tuple
                A tuple containing the wire path to connect gate_a and gate_b.
        """

        connection = []

        # Get position and goal nodes
        position = self.graph.nodes[(gate_a.xcoord, gate_a.ycoord, gate_a.zcoord)]
        goal = self.graph.nodes[(gate_b.xcoord, gate_b.ycoord, gate_b.zcoord)]

        # Add position
        connection.append((position.xcoord, position.ycoord, position.zcoord))

        # Iterate until connection has been made
        while position != goal:

            # Store current position in temporary value
            tmp = position

            # Get next posotion
            position = self.next_position(position, goal)

            # Update wire path and coordinates
            self.wire.update_path(tmp, position)
            self.wire.update_coords(position)

            # Append connection
            connection.append((position.xcoord, position.ycoord, position.zcoord))

        return tuple(connection)

    def cost(self):
        """ Returns current wire cost according to objective function. 
        
        Returns
        -------
        int
                An integer containing the current wire cost.
        """

        length = self.wire.compute_length()
        intersections = self.wire.compute_intersections()

        cost = length + 300 * intersections

        return cost

    def run(self):
        """
        Returns dict with the wire route to connect all gates according to netlist.

        Returns
        -------
        dict 
                A dictionary containing the route of the wire per connection.
        """

        route = {}
        gates = list(self.graph.gates.values())
        # netlist = list(self.graph.netlist)
        completed = set()

        # Iterate over gates
        while gates:

            # Get next gate object
            gate = self.get_next_gate(gates)
            
            if gate in self.graph.connections:

                for connection in self.graph.connections[gate]:

                    combination = tuple(sorted([gate.gateID, connection.gateID]))
                    if combination not in completed:

                        # Get connection
                        connections = self.graph.connections[gate]

                        for connection in connections:
                            connection = self.get_next_connection(connections)

                            # Get corresponding Gate objects
                            gate_a, gate_b = gate, connection
                            combination = tuple(sorted((gate_a.gateID, gate_b.gateID)))

                            while connections:
                                
                                a, b = gate, connection
                                route[combination] = self.make_connection(a, b)
                                completed.add(combination)

        # Calculate wire cost
        cost = self.wire.compute_costs()
        print(f'Cost = {cost}')

        return route

'***************************************************************************'

