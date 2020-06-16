from collections import Counter

class Wire():

    def __init__(self):
        """Initializes a Wire object."""

        # Keeps track of wire path for check collision and computation costs
        self.path = set() 

        # Keeps track of coordinates for computation itersections
        self.coords = []

    def update_path(self, position, step):
        """Updates the wire path."""

        # Get position and step coordinates
        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord

        # Sort and convert to tuple to ensure consistent order
        path = tuple(sorted((position_coords, step_coords)))

        self.path.add(path)

    def update_coords(self, position):
        """Updates the wire coordinates.
        
        Only append nodes who are not a gate, because gates cannot cause
        intersections.
        """

        if position.isgate is False:
            self.coords.append(position)

    def check_collision(self, position, step):
        """Returns True if no collision occurs, otherwise False."""

        # Get position and step coordinates
        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord

        # Sort and convert to tuple to ensure consistent order
        step = tuple(sorted((position_coords, step_coords)))

        return step not in self.path

    def compute_length(self):
        """Returns the length of the wire."""

        return len(self.path)

    def compute_intersections(self):
        """Returns the number of intersection.

        Intersection is indicated when an node, who is not a gate, occurs
        more than once. The occurance is decremented by 1 to count the 
        occurance of intersections and not the occurance of a node.
        """
        
        # Counts occurences of coordinates
        counter = Counter(self.coords)
        print(counter)

        # Compute number of intersections
        intersections = 0
        for coordinate in counter:
            if counter[coordinate] > 1:
                intersections += counter[coordinate] - 1

        return intersections

    def compute_costs(self):
        """Returns the costs of the wire."""

        length = self.compute_length()
        intersections = self.compute_intersections()

        return length + 300 * intersections

    