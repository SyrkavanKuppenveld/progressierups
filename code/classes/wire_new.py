from collections import Counter

class Wire():

    def __init__(self):

        self.path = set()
        self.coords = []

    def update_path(self, position, step):
        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord
        step = tuple(sorted((position_coords, step_coords)))

        self.path.add(step)

    def update_coords(self, position):

        if position.isgate is False:
            self.coords.append(position)

    def check_collision(self, position, step):
        """Returns True if no collision occurs, otherwise False."""

        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord
        step = tuple(sorted((position_coords, step_coords)))

        return step not in self.path

    def compute_length(self):
        """Returns the length of the wire."""

        return len(self.path)

    def compute_intersections(self):
        """Returns the number of intersection."""

        # Counts occurences of coordinates
        counter = Counter(self.coords)

        # Compute number of intersections
        intersections = 0
        for coordinate in counter:
            if counter[coordinate] > 1:
                print(counter[coordinate])
                intersections += counter[coordinate] - 1

        return intersections

    def compute_costs(self):
        """Returns the costs of the wire."""

        length = self.compute_length()
        print(length)
        intersections = self.compute_intersections()
        print(intersections)

        return length + 300 * intersections

    