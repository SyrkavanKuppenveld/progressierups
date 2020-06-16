from code.algorithms import Random_GreedyNet

class Random_GreedyNet_LookAhead(Random_GreedyNet):
    """ Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance with a 4 step look ahead. 

    The algorithm is random because the order in which the connections are made is
    randomly generated. Moreover, if multiple steps have the minimal distance, the
    next step is randomly generated. The algorithm is greedy because it will 
    choose the gate with the lowest Manhattan distance with a 4 step look ahead. 
    """

    def next_position(self, position, goal):
        """Returns next position occuring to 4 steps look ahead."""

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
            # first iteration, however, this this should not be included as a depth level
            elif len(state) < depth + 1:
                
                # Assign next position according to first
                if first:
                    position_next = position
                else:
                    position_next = state[len(state) - 1]

                # Iterate over neighbors current position
                for i in position_next.neighbors:
     
                    # Different approach for first iteration
                    if first:
                        child = [position_next.copy(), i.copy()]

                        # Return position if goal gate is reached
                        if (i.xcoord, i.ycoord, i.zcoord) == (goal.xcoord, goal.ycoord, goal.zcoord):

                            # Get corresponding position from original graph nodes
                            position = self.graph.nodes[(i.xcoord, i.ycoord, i.zcoord)]
                            return position

                        # Only append path if no collission occurs
                        elif self.wire.check_collision(position_next, i):
                            stack.append(child)
                    else:
                        child = self.copy_nodes(state)

                        # Only append if i is valid
                        if self.path_check(child, i, position_next) and self.valid_check(child, i):
                            child.append(i)
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
        """Returns a 'deep' copy of list of nodes."""

        copy = []
        for node in state:
            node_copy = node.copy()
            copy.append(node_copy)

        return copy

    def path_check(self, child, i, position):
        """Returns True if path is valid, otherwise False."""

        # Returns False if collision occurs
        if self.wire.check_collision(position, i) is False:
            # print(self.wire.check_collision(position, i))
            return False
        
        # Returns False if i is in child
        i_coords = i.xcoord, i.ycoord, i.zcoord
        for node in child:
            node_coords = node.xcoord, node.ycoord, node.zcoord
            if i_coords == node_coords:
                return False
        
        return True

    def valid_check(self, child, i):
        """Returns True if move is valid, otherwise False."""

        # Get coordinates of i
        i_x, i_y, i_z = i.xcoord, i.ycoord, i.zcoord

        # Get coordinates of last position in child
        last = len(child) - 1
        child_x, child_y, child_z = child[last].xcoord, child[last].ycoord, child[last].zcoord

        # Compute absolute difference between 
        x_diff = abs(child_x - i_x)
        y_diff = abs(child_y - i_y)
        z_diff = abs(child_z - i_z)
        abs_diff = x_diff + y_diff + z_diff

        return abs_diff == 1 and x_diff < 2 and y_diff < 2 and z_diff < 2

    def path_distance(self, path, goal):
        """Returns the Manhattan Distance for total path."""
        
        dist = 0
        for i, step in enumerate(path):
            if i > 0:
                dist += self.compute_manhattan_dist(step, goal)

        return dist

    def all_distances(self, paths, goal):
        """Returns the list with all distances and their corresponding total distance."""

        mdist = []

        for path in paths:
            total_dist = self.path_distance(path, goal)
            mdist.append((path[1], total_dist))

        return mdist