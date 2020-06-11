

class Greedy():

    def __init__(self, gates, connections):
        """Initializes a Greedy object."""

        gates = self.gates
        connections = self.connections

    def get_nextGate(self):

        # Compute gate density
        for gate in self.gates:
            self.gates[gate].get_density(False)

        
        
        

        pass

    def run(self):
        pass