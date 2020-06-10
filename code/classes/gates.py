import csv

class Gate():
    """"""

    def __init__(self, gateID, gateLetter, xcoord, ycoord):
        """Initialize Gate object."""

        self.gateID = gateID
        self.gateLetter = gateLetter
        self.xcoord = int(xcoord)
        self.ycoord = int(ycoord)

    # def __hash__(self):
    #     return hash(self.gateID)
            
    