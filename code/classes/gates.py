import csv

class Gate():
    """"""

    def __init__(self, gateID, gateLetter, xcoord, ycoord, connections):
        """Initialize Gate object."""

        self.gateID = gateID
        self.gateLetter = gateLetter
        self.xcoord = int(xcoord)
        self.ycoord = int(ycoord)
        self.status = self.startStatus(connections)

    def startStatus(self, connections):
        """Returns a dict with the start status of completed connections."""
        
        status = {}

        for gate in connections:
            status[gate] = False

        return status

    def updateStatus(self, gate):
        """Sets the connection to True if connection is completed."""

        self.status[gate] = True
            
    