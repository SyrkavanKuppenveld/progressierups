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
    Depth of 4.
    """

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
        if neighbor.intersections > 0:
            return False
        
        # Returns False if i is in child
        neighbor_coords = neighbor.xcoord, neighbor.ycoord, neighbor.zcoord
        neighbor_node = self.graph.nodes[neighbor_coords]
        if neighbor_node in child:
            return False
        