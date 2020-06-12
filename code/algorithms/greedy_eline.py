import random

class Random():

<<<<<<< HEAD
class Greedy_eline():

    def __init__(self, gates, connections):
=======
    def __init__(self, graph):
>>>>>>> b104d1b58951bc8595f6e70127da6b18d1b29f01
        """Initializes a Greedy object."""
        pass
    #     gates = self.gates
    #     connections = self.connections

<<<<<<< HEAD
    # def get_nextGate(self):

    #     # Compute gate density
    #     for gate in self.gates:
    #         self.gates[gate].get_density(False)
=======
        self.graph = graph

    def get_next_gate(self, gates):
        """Gets random gate and removes it from the list."""

        gates.pop(random.randrange(0, len(gates)))

        return gates.pop()

    def run(self):

        gates = list(self.graph.gates.values())
        connections_made =  set()

        while gates:
            gateID = self.get_next_gate(gates)
            gate = self.graph.gates[gateID] 

            for connection in self.graph.connections[gate]:

                gate_a, gate_b = gate, connection

                combination = tuple(sorted(gate_a, gate_b))

                if combination not in connections_made:

                    # Get gate coordinates
                    gate_a_x, gate_a_y, gate_a_z = gate_a.xcoord, gate_a.ycoord. gate_a.zcoord
                    gate_b_x, gate_b_y, gate_a_Z = gate_b.xcoord, gate_b.ycoord, gate_b.zcoord


                    start_coords = (gate_a_x, gate_a_y, gate_a_z)


                




>>>>>>> b104d1b58951bc8595f6e70127da6b18d1b29f01


    #     pass

<<<<<<< HEAD
    # def run(self):
    #     pass
=======

class Greedy(Random):

    def get_next_gate(self):

        # Compute gate density
        for gate in self.graph.gates:
            self.graph.gates[gate].get_density(False)

        gates = self.graph.gates.sort(key=lambda gate: gate.density)

        return gates.pop()
>>>>>>> b104d1b58951bc8595f6e70127da6b18d1b29f01
