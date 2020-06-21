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


"""
Code for a Greedy Algorithm.


This module contains the code for the Greedy algorithm and the extentions on the
algorithm. The exentions are: 
* LookAhead: with a 4 step depth look a head.
* NoIntersect: intersections as hard constrained.
* NoIntersectLookAhead: intersections as hard constrained and a 4 step look a head.
* LookAheadCosts: different costs formula.
"""

from code.classes import Wire
from code.visualization.visualize import Chip_Visualization
import random
import copy

class Greedy():
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

    def __init__(self, graph, order, approach):
        """
        Initializes the Random Greedy Net algorithm.
        
        Parameters
        ----------
        graph: a Graph object
                A Graph object representing the chip grid.
        """
 
        self.graph = graph
        self.order = order 
        self.wire = Wire()
        self.approach = approach

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

        # Assign new position
        position = self.get_random_min(mdist)

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
        
        return wire_path

    def run(self):
        """
        Returns a dictionary with the wire route to connect all gates according to netlist.

        Returns
        -------
        dict 
                A dictionary containing the route of the wire per connection.
        """
        
        if self.approach is True:
            route = {}
            
            # Repeat run until solution is found
            not_found = True
            while not_found:
                try:

                    # Make deep copy of connection order
                    connections = copy.deepcopy(self.order)

                    # Iterate until netlist is empyt
                    while connections:

                        # Get random connection 
                        connection = connections.pop(0)

                        # Get corresponding Gate objects
                        a, b = connection[0], connection[1]
                        gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

                        # Generate the connection between gate a and b
                        route[(a, b)] = self.make_connection(gate_a, gate_b)

                    # Set not_found to Flase   
                    not_found = False
                except ValueError:

                    # Clear graph, wire and route
                    self.graph.clear_graph()
                    self.wire = Wire()
                    route = {}

            return route

        else:
            route = {}
            completed = set()
            
            # Repeat run until solution is found
            not_found = True
            while not_found:
                try:

                    # Make deep copy of connection order
                    gates = copy.deepcopy(self.order)

                    # Iterate until netlist is empyt
                    while gates:

                        # Get gate object and corresponding connections
                        gateID = gates.pop(0)
                        gate_a = self.graph.gates[gateID]

                        # Check if gate_a in connections
                        if gate_a in self.graph.connections:

                            # Get corresponding connections
                            connections = self.graph.connections[gate_a]

                            # Iterate until connections is empty
                            while connections:

                                # Generate next connection
                                gate_b = connections.pop()

                                # Check if connection is already completed
                                a, b = gate_a.gateID, gate_b.gateID
                                connection = tuple(sorted((a, b)))
                                if connection not in completed:
            
                                    # Generate the connection between gate a and b
                                    route[(a, b)] = self.make_connection(gate_a, gate_b)

                                    # Add connection to completed
                                    completed.add(connection)

                    # Set not_found to Flase   
                    not_found = False
                except ValueError:

                    # Clear graph, wire and route
                    self.graph.clear_graph()
                    self.wire = Wire()
                    route = {}
                    completed = set()

            return route


class GreedyLookAhead(Greedy):
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

    Look ahead
    ----------
    Depth of 4.

    """

    def next_position(self, position, goal):
        """
        Returns next position according to 4 steps look ahead.

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

        depth = 4
        stack = [[]]
        paths = []

        # Set first to True
        first = True

        # Iterate until the stack is empty
        while len(stack) > 0:
            state = stack.pop()

            # Append the state to path if first iteration is false and it reached the goal 
            # gate or if state length equals the depth
            length = len(state)
            if first is False and (length == depth + 1 or state[length - 1] == goal):
                paths.append(state)

            # Only continue if len state does not exceed the depth
            # depth + 1 >> because the current position is also added to the state in the
            # first iteration, however, this should not be included as a depth level
            elif len(state) < depth + 1:
                
                # Assign next position according to first
                if first:
                    position_next = position
                else:
                    position_next = state[len(state) - 1]

                # Iterate over neighbors of the current position
                for neighbor in position_next.neighbors:
     
                    # Different approach for first iteration
                    if first:
                        child = [position_next.copy(), neighbor.copy()]

                        # Return position if goal gate is reached and no collision is caused
                        if (neighbor.xcoord, neighbor.ycoord, neighbor.zcoord) == (goal.xcoord, goal.ycoord, goal.zcoord) and self.wire.check_collision(position_next, neighbor):

                            # Get corresponding position from original graph nodes
                            position = self.graph.nodes[(neighbor.xcoord, neighbor.ycoord, neighbor.zcoord)]
                            return position

                        # Only append path if no collission occurs
                        elif self.wire.check_collision(position_next, neighbor):
                            stack.append(child)
                    else:
                        child = self.copy_nodes(state)

                        # Only append if i is valid
                        if self.path_check(child, position_next, neighbor) and self.valid_check(child, neighbor):
                            child.append(neighbor)
                            stack.append(child)

                # Set first to False
                first = False

        # Generate list with all path distances
        mdist = self.all_distances(paths, goal)

        # Get next position 
        position = self.get_random_min(mdist)

        # Get corresponding position from orginal graph nodes
        position = self.graph.nodes[(position.xcoord, position.ycoord, position.zcoord)]

        return position

    def copy_nodes(self, state):
        """
        Returns a 'deep' copy of list of nodes.

        Parameters
        ----------
        state: a list
                A list containing Node objects representing a wire path.

        Returns 
        -------
        list
                A list containing 'deep' copy of the nodes in the original list.
        """

        copy = []
        for node in state:
            node_copy = node.copy()
            copy.append(node_copy)

        return copy

    def path_check(self, child, position, neighbor):
        """
        Returns True if path is valid, otherwise False.
        
        Parameters
        ----------
        child: a list 
                A list containing Node objects representing a wire path.

        position: a Node object
                 A node object representing the current position of the wire in the grid.

        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.

        Returns 
        -------
        boolchec
                True if successfull, otherwise False.
        """

        neighbor_coords = neighbor.xcoord, neighbor.ycoord, neighbor.zcoord
        neighbor_node = self.graph.nodes[neighbor_coords]

        return self.wire.check_collision(position, neighbor) and neighbor_node not in child

    def valid_check(self, child, neighbor):
        """
        Returns True if move is valid, otherwise False.
        
        Parameters
        ----------
        child: a list 
                A list containing Node objects representing a wire path.

        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.

        Returns 
        -------
        bool
                True if successfull, otherwise False.
        """

        # Get coordinates of neighbor
        neighbor_x, neighbor_y, neighbor_z = neighbor.xcoord, neighbor.ycoord, neighbor.zcoord

        # Get coordinates of last position in child
        last = len(child) - 1
        child_x, child_y, child_z = child[last].xcoord, child[last].ycoord, child[last].zcoord

        # Compute absolute difference between child and neighbor
        x_diff = abs(child_x - neighbor_x)
        y_diff = abs(child_y - neighbor_y)
        z_diff = abs(child_z - neighbor_z)
        abs_diff = x_diff + y_diff + z_diff

        return abs_diff == 1 and x_diff < 2 and y_diff < 2 and z_diff < 2

    def all_distances(self, paths, goal):
        """
        Returns the list with all distances and their corresponding total costs.
        
        Parameters
        ----------
        path: a list
                A list containing all valid paths for a for step look ahead.

        goal: a Node object
                A Node object repesenting the goal position on the grid.

        Returns 
        -------
        list        
                A list with tuples. First element of tuple is the neighbor and the 
                second element is the path's costs. 
        """

        costs = []

        for path in paths:
            total_dist = self.path_distance(path, goal)
            costs.append((path[1], total_dist))

        return costs

    def path_distance(self, path, goal):
        """
        Returns the Manhattan Distance for total path.
        
        Parameters
        ----------
        path: a list
                A list of Nodes representing a wire path.

        goal: a Node object
                A Node object repesenting the goal position on the grid.

        Returns 
        -------
        int
                The Manhattan Distance of the total path.
        """
        
        dist = 0
        for i, step in enumerate(path):
            if i > 0:
                dist += self.compute_manhattan_dist(step, goal)

        return dist


class GreedyNoIntersect(Greedy):
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. For this algorithm intersections
    are a hard constraint. 

    Random element
    --------------
    * The order of the connections are generated randomly.
    * If multiple neighbors have the same distance, the next position is generated
      randomly. 
    
    Greedy element
    --------------
    The next position will be the neighbor with the lowest Manhattan distance.
    """

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
            if self.wire.check_collision(position, neighbor) and neighbor.intersection == 0 and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                mdist.append((neighbor, dist))
                  
        # Assign new position
        position = self.get_random_min(mdist)

        return position

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
        
        return tuple(wire_path)


class GreedyNoIntersectLookAhead(GreedyNoIntersect):
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. For this algorithm intersections
    are a hard constraint. 

    Random element
    --------------
    * The order of the connections are generated randomly.
    * If multiple neighbors have the same distance, the next position is generated
      randomly. 
    
    Greedy element
    --------------
    The next position will be the neighbor with the lowest Manhattan distance.

    Look ahead
    ----------
    Depth of 5.
    """

    def next_position(self, position, goal):
        """
        Returns next position occuring to 4 steps look ahead.

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
        """

        depth = 4
        stack = [[]]
        paths = []

        # Set first to True
        first = True

        # Iterate until the stack is empty
        while len(stack) > 0:
            state = stack.pop()

            # Append the state to path if first iteration is false and it reached the goal 
            # gate or state length equals the depth
            length = len(state)
            if first is False and (length == depth + 1 or state[length - 1] == goal):
                paths.append(state)

            # Only continue if len state does not exceed the depth
            # depth + 1 >> because the current position is also added to the state in the
            # first iteration, however, this should not be included as a depth level
            elif len(state) < depth + 1:
                
                # Assign next position according to first
                if first:
                    position_next = position
                else:
                    position_next = state[len(state) - 1]

                # Iterate over neighbors current position
                for neighbor in position_next.neighbors:
     
                    # Different approach for first iteration
                    if first:
                        child = [position_next.copy(), neighbor.copy()]

                        # Return position if goal gate is reached and no collision is caused
                        if (neighbor.xcoord, neighbor.ycoord, neighbor.zcoord) == (goal.xcoord, goal.ycoord, goal.zcoord) and self.wire.check_collision(position_next, neighbor):

                            # Get corresponding position from original graph nodes
                            position = self.graph.nodes[(neighbor.xcoord, neighbor.ycoord, neighbor.zcoord)]
                            return position

                        # Only append neighbor if no collission or intersection occurs
                        elif self.wire.check_collision(position_next, neighbor) and neighbor.intersection == 0:
                            stack.append(child)
                    else:
                        child = self.copy_nodes(state)

                        # Only append if neighbor is valid
                        if self.path_check(child, position_next, neighbor) and self.valid_check(child, neighbor):
                            child.append(neighbor)
                            stack.append(child)

                # Set first to False
                first = False

        # Generate list with all path distances
        mdist = self.all_distances(paths, goal)

        # Get next position 
        position = self.get_random_min(mdist)

        # Get corresponding position form orginal graph nodes
        position = self.graph.nodes[(position.xcoord, position.ycoord, position.zcoord)]

        return position


    def copy_nodes(self, state):
        """
        Returns a 'deep' copy of list of nodes.

        Parameters
        ----------
        state: a list
                A list containing Node objects representing a wire path.

        Returns 
        -------
        list
                A list containing 'deep' copy of the nodes in the original list.
        
        """

        copy = []
        for node in state:
            node_copy = node.copy()
            copy.append(node_copy)

        return copy

    def path_check(self, child, position, neighbor):
        """
        Returns True if path is valid, otherwise False.
        
        Parameters
        ----------
        child: a list 
                A list containing Node objects representing a wire path.

        position: a Node object
                A node object representing the current position of the wire in the grid.

        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.

        Returns 
        -------
        bool
                True if successfull, otherwise False.
        
        """

        # Returns False if collision occurs
        if self.wire.check_collision(position, neighbor) is False:
            return False
        
        # Return False if intersection will occur if neighbor is appended to path
        if neighbor.intersection != 0:
            return False
        
        # Returns False if neighbor is in child
        neighbor_coords = neighbor.xcoord, neighbor.ycoord, neighbor.zcoord
        neighbor_node = self.graph.nodes[neighbor_coords]
        if neighbor_node in child:
            return False

        return True

    def valid_check(self, child, neighbor):
        """
        Returns True if move is valid, otherwise False.
        
        Parameters
        ----------
        child: a list 
                A list containing Node objects representing a wire path.

        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.

        Returns 
        -------
        bool
                True if successfull, otherwise False.
        
        """

        # Get coordinates of neighbor
        neighbor_x, neighbor_y, neighbor_z = neighbor.xcoord, neighbor.ycoord, neighbor.zcoord

        # Get coordinates of last position in child
        last = len(child) - 1
        child_x, child_y, child_z = child[last].xcoord, child[last].ycoord, child[last].zcoord

        # Compute absolute difference between child and neighbour
        x_diff = abs(child_x - neighbor_x)
        y_diff = abs(child_y - neighbor_y)
        z_diff = abs(child_z - neighbor_z)
        abs_diff = x_diff + y_diff + z_diff

        return abs_diff == 1 and x_diff < 2 and y_diff < 2 and z_diff < 2

    def all_distances(self, paths, goal):
        """
        Returns the list with all distances and their corresponding total distance.
        
        Parameters
        ----------
        path: a list
                A list containing all valid paths for a for step look ahead.

        Goal: a Node object
                A Node object repesenting the goal position on the grid.

        Feturns 
        -------
                A list with tuples. First element of tuple is the neighbor and the 
                second element is the Manhattan distance. 

        """

        mdist = []

        for path in paths:
            total_dist = self.path_distance(path, goal)
            mdist.append((path[1], total_dist))

        return mdist

    def path_distance(self, path, goal):
        """
        Returns the Manhattan Distance for total path.
        
        Parameters
        ----------
        path: a list
                A list of Nodes representing a wire path.

        Goal: a Node object
                A Node object repesenting the goal position on the grid. 

        Returns 
        -------
        int
                The Manhattan Distance of the total path.
        
        """
        
        dist = 0
        for i, step in enumerate(path):
            if i > 0:
                dist += self.compute_manhattan_dist(step, goal)

        return dist


class GreedyLookAheadCosts(GreedyLookAhead):
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

    Look ahead
    ----------
    Depth of 4.

    Costs
    -----
    The cost assigned to the step are higher if the step and its neighbors already 
    are wired. In order to avoid this places on the grid. 
    """

    def compute_wire_costs(self, step, goal):
        """
        Returns the increase in wire costs of the step.

        Parameters 
        ----------
        step: a Node object
                A Node object representing the next position of the wire.

        goal: a Node object
                A Node object representing the goal position on the grid.
            
        Returns
        -------
        int 
                The wire costs of the step.
        """
        
        # Get the coordinates of step and goal
        step_coords = step.xcoord, step.ycoord, step.zcoord
        goal_coords = goal.xcoord, step.ycoord, step.zcoord

        cost = 0

        # Only add extra costs if step is not goal
        if step_coords != goal_coords:

            # Increment the cost with 5 if the step with cause intersection
            if step.zcoord == 0:
                cost += 10
            elif step.zcoord == 1:
                cost += 5

            # 
            if step.intersection > 0:
                cost += 10

            # Increment the costs with 2 per neighbor of the step who is alread wired
            for neighbor in step.neighbors:
                if neighbor.intersection > 0:
                    cost += 2

        return cost

    def compute_total_costs(self, step, goal):
        """
        Returns the costs of the step according to the Manhattan Distance and the 
        wire costs.

        Parameters 
        ----------
        position: a Node object
                A Node object representing the current position of the wire.

        step: a Node object
                A Node object representing the next position of the wire.

        goal: a Node object
                A Node object repesenting the goal position on the grid.

        Returns
        -------
        int 
                The costs of the path.
        """

        # Compute Manhattan Distance between position and goal
        mdist = self.compute_manhattan_dist(step, goal)
        
        # Compute wire costs
        wire_cost = self.compute_wire_costs(step, goal)

        return mdist + wire_cost

    def path_distance(self, path, goal):
        """
        Returns the total costs of the total path.
        
        Parameters
        ----------
        path: a list
                A list of Nodes representing a wire path.

        goal: a Node object
                A Node object repesenting the goal position on the grid.

        Returns 
        -------
        int
                The costs of the total path.
        
        """
        
        dist = 0
        for i, step in enumerate(path):
            if i > 0:
                dist += self.compute_total_costs(step, goal)

        return dist


        