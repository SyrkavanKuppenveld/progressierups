from code.classes import Wire
from code.visualization.visualize import Chip_Visualization
import random
import copy

class Random_GreedyNet():
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

    def next_position(self, position, goal):
        """Returns the next position."""

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
        """Returns step with lowest Manhattan Distance, if multiple it returns
        one randomly.
        """
        
        min_value = min(lst, key=lambda x: x[1])
        minimum = []
        for dist in lst:
            if dist[1] == min_value[1]:
                minimum.append(dist[0])

        return random.choice(minimum)

    def make_connection(self, gate_a, gate_b):
        """Returns wire connection between gate_a and gate_b."""
        
        connection = []

        # Get position and goal nodes
        position = self.graph.nodes[(gate_a.xcoord, gate_a.ycoord, gate_a.zcoord)]
        goal = self.graph.nodes[(gate_b.xcoord, gate_b.ycoord, gate_b.zcoord)]

        # Add position
        connection.append((position.xcoord, position.ycoord, position.zcoord))

        # Iterate until connection has been made
        while (position.xcoord, position.ycoord, position.zcoord) != (goal.xcoord, goal.ycoord, goal.zcoord):
            
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
   
    def run(self):

        route = {}
        netlist = list(self.graph.netlist)

        while netlist:

            # Get random connection 
            connection = netlist.pop(random.randrange(0, len(netlist)))

            # Get corresponding Gate objects
            a, b = connection[0], connection[1]
            gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

            # Generate the connection between gate a and b
            route[(a, b)] = self.make_connection(gate_a, gate_b)

        return route


class Random_GreedyNet_LookAhead(Random_GreedyNet):

    def next_position(self, position, goal):
        """Returns next position occuring to x steps look ahead."""

        depth = 4
        stack = [[]]
        paths = []

        first = True

        while len(stack) > 0:
            state = stack.pop()

            # Check if goal gate is reached
            length = len(state)
            if first is False and (length == depth + 1 or state[length - 1] == goal):
                paths.append(state)

            #
            elif len(state) < depth + 1:
                
                # Assign next position according to first
                if first is False:
                    position_next = state[len(state) - 1]


                else:
                    position_next = position

                # Iterate over neighbors current position
                for i in position_next.neighbors:
                    # print(f'i = {i}')

                    # Assign child according to first
                    if first:
                        child = [position_next.copy(), i.copy()]

                        # Check collision
                        if (i.xcoord, i.ycoord, i.zcoord) == (goal.xcoord, goal.ycoord, goal.zcoord):
                            position = self.graph.nodes[(i.xcoord, i.ycoord, i.zcoord)]
                            return position
                        elif self.wire.check_collision(position_next, i):
                            stack.append(child)
                    else:
                        child = self.copy_nodes(state)

                        # Ensure path is valid
                        if self.path_check(child, i, position_next) and self.valid_check(child, i):
                            child.append(i)
                            stack.append(child)

                first = False

        # Generate list with all path distances
        mdist = self.all_distances(paths, goal)

        # Get next position
        position = self.get_random_min(mdist)
        position = self.graph.nodes[(position.xcoord, position.ycoord, position.zcoord)]

        return position


    def copy_nodes(self, state):
        """Returns a true copy of a node."""
        copy = []
        for node in state:
            node_copy = node.copy()
            copy.append(node_copy)

        return copy

    def path_check(self, child, i, position):
        """Returns True if node is unique in path, False otherwise."""

        if self.wire.check_collision(position, i) is False:
            # print(self.wire.check_collision(position, i))
            return False
        
        i_coords = i.xcoord, i.ycoord, i.zcoord
        for node in child:
            node_coords = node.xcoord, node.ycoord, node.zcoord
            if i_coords == node_coords:
                return False
        
        return True

    def valid_check(self, child, i):
        """Returns True if move is valid, otherwise False."""

        i_x, i_y, i_z = i.xcoord, i.ycoord, i.zcoord
        if len(child) == 1:
            last = 0
        else:
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
        """Returns the list """

        mdist = []

        for path in paths:
            total_dist = self.path_distance(path, goal)
            mdist.append((path[1], total_dist))

        return mdist

