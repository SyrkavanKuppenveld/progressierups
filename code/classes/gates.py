import csv

class Gate():
    def __init__(self, gateID, gateLetter, xcoord, ycoord):
        self.gateID = gateID
        self.gateLetter = gateLetter
        self.xcoord = int(xcoord)
        self.ycoord = int(ycoord)


    def get_connections(self):
        pass 

    