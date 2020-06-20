from code.algorithms_revised import Greedy

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