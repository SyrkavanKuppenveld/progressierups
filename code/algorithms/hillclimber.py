from code.classes import Graph
from code.algorithms import Greedy_RandomNet_LookAhead, Greedy_RandomNet
from code.visualization import Chip_Visualization
import random

class HillClimber(Greedy_RandomNet_LookAhead):
    """
    <INFORMATIE>
    """

    def __init__(self, graph, random_startState, start_wire_path, start_cost):
        """ 
        Initializes the start state of the algorithm.
        """

        # 1. Initialize a random start state
        # Keeps track of current state
        self.graph = graph
        self.wire = random_startState
        self.wire_path = start_wire_path
        self.cost = start_cost

        # Keeps track of best state
        self.best_graph = graph
        self.best_wire = random_startState
        self.best_wire_path = start_wire_path
        self.best_cost = start_cost

        # Used to check on conversion
        self.improvements = []
        self.conversion = False

    def get_random_net(self):
        
        # Randomly choose a net that is to be re-build
        nets = list(self.wire_path.keys())
        net = random.choice(nets)
        
        gate_a = self.graph.gates[net[0]]
        gate_b = self.graph.gates[net[1]]

        gates = (gate_a, gate_b)

        return net, gates
    
    def remove_net(self, net, gates):
        
        net_path = self.wire_path[net]
        
        # coord_storage = []
        for coordinates in net_path:    
            # Remove old path coordinates from the coordinate storage of the Wire Object
            # Gates can never be an intersection and thus will not be taken into account
            node = self.graph.nodes[coordinates]
            if not node.isgate:
                # Remove node form coordinate storage
                self.wire.coords.remove(node)

                # Correct intersection-count of the Node object of the current coordinate
                node.decrement_intersection()
        
        # Remove old wire units from the path storage of the Wire Object
        for i, coordinate in enumerate(net_path):
            if i > 0:
                combination = tuple(sorted((net_path[i - 1], net_path[i])))
                self.wire.path.remove(combination)

    def apply_random_adjustment(self, net, gates):
        
        gate_a, gate_b = gates
        new_path = self.make_connection(gate_a, gate_b)

        # Update wire_path
        self.wire_path[net] = new_path

    def run(self):
        ITERATIONS = 100
        count = 0

        # --------------------- Visualise Chip ---------------------
        visualisation = Chip_Visualization(self.graph.gates, self.wire_path)
        visualisation.run()
        
        # 2. Repeat until cost does not improve after N iterations:
        while not self.conversion:
            
            # 3. Apply random adjustment
            # Get random net
            net, gates = self.get_random_net()

            # Remove old net path form wire object
            self.remove_net(net, gates)

            # Apply random adjustment on net
            self.apply_random_adjustment(net, gates)

            # Compute cost of adjusted state
            cost = self.wire.compute_costs()

            # 4. If state improved (cost decreased):
            if cost < self.best_cost:
                # 5. Confirm adjustment
                self.best_cost = cost
                self.best_graph = self.graph
                self.best_wire = self.wire
                self.best_wire_path = self.wire_path
                self.improvements.append(True)
            else:
                self.improvements.append(False)

            count += 1

            # Check if conversion has occured over the past 20 iterations
            if len(self.improvements) == ITERATIONS:
                # If no improvement occured, quit the HillClimber algorithm
                if True not in self.improvements:
                    break

                # Make room for next iteration
                self.improvements.pop(0)
        
            # --------------------- Visualise Chip ---------------------
            visualisation = Chip_Visualization(self.graph.gates, self.wire_path)
            visualisation.run()

            


        