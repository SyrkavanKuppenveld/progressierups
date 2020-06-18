from code.algorithms.greedy_randomnet_lookahead import Greedy_RandomNet_LookAhead

class GreedyDensity_LookAhead(Greedy_RandomNet_LookAhead):
    """ 
    Creates a Wire object that connects the gates according to the netlist and 
    according to the lowest Manhattan Distance. 

    Random element
    --------------
    * If multiple neighbors have the same distance, the next position is generated
      randomly. 
    
    Greedy element
    --------------
    The next position will be the neighbor with the lowest Manhattan distance. The
    order of the gate is from max to min density. Density refers to the amount of
    other gates which lie within a specified radius of the gate. The radius differs
    per chip. 

    Look ahead
    ----------
    Depth of 4.
    """

    def run(self):
        """
        Returns a dictionary with the wire route to connect all gates according to netlist.

        Returns
        -------
        dict 
                A dictionary containing the route of the wire per connection.
        """

        route = {}
        gates_density = self.graph.compute_densities(3)
        completed = set()

        # Iterate until netlist is empyt
        while gates_density:

            # Get gates based on density
            gateID = gates_density.pop(0)[0]
            gate = self.graph.gates[gateID]

            if gate in self.graph.connections:

                # Iterate over the connections of the gate
                for connection in self.graph.connections[gate]:

                    # Check if connection is not already completed
                    combination = tuple(sorted([gate.gateID, connection.gateID]))
                    if combination not in completed:

                        # Get corresponding Gate objects             
                        gate_a, gate_b = gate, connection

                        # Generate the connection between gate a and b
                        route[combination] = self.make_connection(gate_a, gate_b)

                    #     # Visualize wire per connection
                    #     visualization = Chip_Visualization(self.graph.gates, route)
                    #     visualization.run()

        return route
