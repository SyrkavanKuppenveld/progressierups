from code.algorithms.greedy_randomnet import Greedy_RandomNet

class Greedy_RandomNet_Astar(Greedy_RandomNet):

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

        path = []

        for neighbor in position.neighbors:

            # Only consider neighbor if it does cause collision
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
            
                # Compute Manhattan Distance from neighbor to goal
                dist = self.compute_manhattan_dist(neighbor, goal)
                
                # Compute costs
                cost = 1
                if neighbor.intersection > 0:
                    cost += 300
                
                # Compute total
                total = dist + cost

                # Append neighbor and total to path
                path.append((neighbor, total))

        # print(path)
                  
        # Assign new position
        position = self.get_random_min(path)

        return position