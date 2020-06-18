from code.algorithms import Greedy_RandomNet_LookAhead

class Greedy_RandomNet_LookAhead_Costs(Greedy_RandomNet_LookAhead):
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
            if step.zcoord < 2:
                cost += 8
            elif step.zcoord >= 2 and step.zcoord < 5:
                cost += 4

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

