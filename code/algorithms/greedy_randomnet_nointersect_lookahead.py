"""
Greedy Random Netlist Without Intersections Look Ahead Algorithm.

This module contains the code for a Greedy Random Netlist Without 
Intersections Look Ahead Algorithm.
"""

from code.algorithms.greedy_randomnet_nointersect import Greedy_RandomNet_NoIntersect


class Greedy_RandomNet_NoIntersect_LookAhead(Greedy_RandomNet_NoIntersect):
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

        depth = 6
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

                        # Return position if goal gate is reached
                        if (neighbor.xcoord, neighbor.ycoord, neighbor.zcoord) == (goal.xcoord, goal.ycoord, goal.zcoord):

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
        