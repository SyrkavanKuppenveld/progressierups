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
        """Returns wire order."""
        
        self.order = []
        total = len(self.netlist)

        for i in range(total):

            # Compute check variable
            check = i % 2
            
            
            if i == 0:
                self.order.append(self.netlist[0][0])
                self.order.append(self.netlist[0][1])
                next_gate = self.netlist[0][1]
                position = 0

            elif check == 1:

                for j, element in enumerate(self.netlist):
                    if next_gate == element[1] and j is not position:
                        self.order.append(element[0])
                        next_gate = element[0]
                        position = j
                        break 

            elif check == 0:
                for j, element in enumerate(self.netlist):
                    if next_gate == element[0] and j is not position:
                        self.order.append(element[1])
                        next_gate = element[1]
                        position = j
                        break 
            
            if i + 1 == total:
                self.order.append(1)
            
            # print(f'check: {check}')
            # print(f'position: {position}')
            # print(f'next gate: {next_gate}')


        # Check print
        print(self.order)

        return self.order

            

    def wire_path(self):

        return 1