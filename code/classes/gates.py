import csv

class Gate():
    def __init__(self, gateID, gateLetter, xcoord, ycoord, connections):
        self.gateID = gateID
        self.gateLetter = gateLetter
        self.xcoord = int(xcoord)
        self.ycoord = int(ycoord)
        self.connections = connections

    