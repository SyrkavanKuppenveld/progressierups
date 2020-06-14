import csv

class Gate():
    """"""

    def __init__(self, gateID, xcoord, ycoord):
        """Initialize Gate object."""

        self.gateID = gateID
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = 0

    # def __repr__(self):
    #     """Ensure that the object is printed properly if it is in a list/dict."""

    #     return str(self.gateID)

    # def __hash__(self):
        
    #     return hash(self.gateID)

    

    # def get_distance(self, distance):
    #     """Assigns gate distances to other gates."""

    #     self.distance = distance

    # def get_density(self, order):
    #     """Computes gate density based on radius k.
    #     If order is True the max density will be computed, when False the min density.
    #     """

    #     distance_sorted = sorted(self.distance, reverse=order)
    #     self.density = sum(distance_sorted)