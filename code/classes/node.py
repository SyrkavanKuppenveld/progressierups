class Node():
    """Creates a Node object which represents a coordinate on the grid."""

    def __init__(self, coords):
        """
        Initializes a Node object.
        
        Parameters
        ----------
        coords: a tuple
                A tuple containing the x-, y- and z-coordates of the grid.
        """

        self.xcoord = coords[0]
        self.ycoord = coords[1]
        self.zcoord = coords[2]
        self.neighbors = set()
        self.isgate = False
        self.intersection = 0
        self.wired_neighbors = 0

    def add_neighbor(self, neighbor):
        """
        Appends neighbor to neighbors.

        Parameters
        ----------
        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.
        """

        self.neighbors.add(neighbor)

    def set_isgate(self):
        """
        Set self.isgate to True.
        """

        self.isgate = True

    def increment_intersection(self):
        """
        Increments self.intersection with 1.
        """

        self.intersection += 1

    def decrement_intersection(self):
        """
        Decrements self.intersection with 1.
        """

        self.intersection -= 1

    def update_neighbors(self):
        """
        Increments self.neighbors with 1.
        """

        self.wired_neighbors += 1

    def copy(self):
        """
        Returns a "deep" copy of the Node.
        
        Returns
        -------
        Node object
                A 'deep' copy of the Node object.
        """

        # Instantiate new node object with same coordinates
        copy = Node((self.xcoord, self.ycoord, self.zcoord))

        # Set all attributes equal to self
        copy.neighbors = self.neighbors
        copy.isgate = self.isgate
        copy.intersection = self.intersection
        copy.wired_neighbors = self.wired_neighbors
        
        return copy

    def __repr__(self):
        """Ensure that the object is printed properly if it is in a list/dict.
        
        Returns
        -------
        str
                The coordinates of the Node object.
        """

        return str((self.xcoord, self.ycoord, self.zcoord))

    

    

    



    
