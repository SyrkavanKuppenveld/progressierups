from code.algorithms.greedy_randomnet import Greedy_RandomNet

class Greedy_RandomNet_NoIntersect(Greedy_RandomNet):
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

            # Update position intersection if position does not contain a gate
            if position.isgate is False:
                position.update_intersection()

            # Append step to wire path
            wire_path.append((position.xcoord, position.ycoord, position.zcoord))
        
        return tuple(wire_path)