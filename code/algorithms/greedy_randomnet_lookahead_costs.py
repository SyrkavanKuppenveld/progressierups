from code.algorithms import Greedy_RandomNet_LookAhead

class Greedy_RandomNet_LookAhead_Costs(Greedy_RandomNet_LookAhead):


    def compute_wire_costs(self, step):
        """
        Returns the increase in wire costs of the step.

        Parameters 
        ----------
        step: a Node object
                A Node object representing the next position of the wire.
            
        Returns
        -------
        int 
                The wire costs of the step.
        """
        
        cost = 1
        if step.intersection > 0:
            cost += 5

        return cost

    def compute_total_costs(self, position, step, goal):
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
        mdist = self.compute_manhattan_dist(position, goal)
        
        # Compute wire costs
        wire_cost = self.compute_wire_costs(step)

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
                dist += self.compute_total_costs(path[0], step, goal)

        return dist

