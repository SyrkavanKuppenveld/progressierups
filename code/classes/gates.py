import csv

class Gate():
    """"""

    def __init__(self, gateID, xcoord, ycoord):
        """Initialize Gate object."""

        self.gateID = gateID
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = 0

    def __repr__(self):
        """Ensure that the object is printed properly if it is in a list/dict."""

        return str(self.gateID)

    # def __hash__(self):
    #     return hash(self.gateID)
