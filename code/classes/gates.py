import csv

class Gate():
    """
    Represents a gate on the grid.
    """

    def __init__(self, gateID, xcoord, ycoord):
        """
        Initialize Gate object.

        Parameters
        ----------
        gateID: int
                Gate ID.

        xcoord: int
                The z-coordinate of the gate.

        ycoord: int
                The y-coordinate of the gate.
        """

        self.gateID = gateID
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = 0

    def __repr__(self):
        """
        Ensure that the object is printed properly if it is in a list/dict.
        
        Return
        ------
        string
                The gate ID.
        """

        return str(self.gateID)

