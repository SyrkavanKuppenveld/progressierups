import numpy as numpy

class Wire():

    def __init__(self, grid, gates, netlist):
        """Initialize Wire object."""

        self.gates = gates
        self.grid = grid
        self.netlist = netlist
        self.start_x = self.gates[1].xcoord
        self.start_y = self.gates[1].ycoord

        self.wire_order = self.wire_gates_order()

    def wire_gates_order(self):
        
        self.order = []
        total = len(self.netlist)

        for i, _ in enumerate(range(total), 1):
            
            if i == 1:
                self.order.append(self.netlist[0][0])
                self.order.append(self.netlist[0][1])
                next_con =  int(self.netlist[0][1]) - 1

            elif total > i:
                self.order.append(self.netlist[next_con][1])
                next_con =  int(self.netlist[next_con][1]) - 1
                print(next_con)

            else:
                # self.order.append(self.netlist[next_con][1])
                # last_con = int(self.netlist[next_con][0]) - 1
                self.order.append(self.netlist[next_con][1])

        print(self.order)

        return self.order

            

    def wire_path(self):

        return 1