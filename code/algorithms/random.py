#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import copy
import random

# Own modules
from code.classes import Graph, Wire

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'


class Random():
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    the lowest Manhattan Distance. 

    Random element
    --------------
    * The order of the connections is generated randomly.
    * The next position is generated randomly.
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
                A list containing the connections of the netlist file.

        Returns
        -------
        tuple
                Randomly generated tuple containing two gates that need to be connected.
        """

        return connections.pop(random.randrange(0, len(connections)))

    def get_next_neighbor(self, neighbors):
        """Randomly returns a neighbour.
        
        Parameters
        ----------
        neighbors: a list
                A list containing the neighbours of the current position of the wire.

        Returns
        -------
        Node object
                Randomly generated neighbour Node.
        """

        return neighbors.pop(random.randrange(0, len(neighbors)))

    def next_position(self, position, goal):
        """
        Returns a random next position.
                
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
            # Get a random next neighbour
            neighbor = self.get_next_neighbor(neighbors)
            # Only return neighbor if a path to this neighbor does not cause a collision
            if self.wire.check_collision(position, neighbor):
                return neighbor

        raise ValueError

    def make_connection(self, gate_a, gate_b):
        """
        Returns a set with the wire path between gate_a and gate_b.
        
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
                A dictionary containing the route of the wire per connection in netlist.
        """

        run_counter = 1

        route = {}

        # Run algorithm until solution is found
        not_found = True
        while not_found:
            try:
                # Make deep copy of netlist
                netlist = copy.deepcopy(list(self.graph.netlist))

                # Iterate until netlist is empyt
                while netlist:

                    # Get random connection 
                    connection = netlist.pop(random.randrange(0, len(netlist)))

                    # Get corresponding Gate objects
                    a, b = connection[0], connection[1]
                    gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

                    # Generate the connection between gate a and b
                    route[(a, b)] = self.make_connection(gate_a, gate_b)

                not_found = False
            except ValueError:

                # Clear graph, wire and route
                self.graph.clear_graph()
                self.wire = Wire()
                route = {}

                # Print restart
                print(f"Restart {run_counter}...")
                run_counter += 1
        
        return route




