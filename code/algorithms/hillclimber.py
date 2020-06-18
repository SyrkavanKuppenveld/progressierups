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
    
        self.graph = graph
        self.wire = random_startState
        self.wire_path = start_wire_path
        self.cost = start_cost
        self.no_improvement_count = 0
        
    def get_random_startState(self):
        pass
        
        # self.wire_path = wire_path
        # self.cost = costs
        # self.wire = algo.wire

    def get_random_net(self):
        
        # Randomly choose a net that is to be re-build
        nets = list(self.wire_path.keys())
        net = random.choice(nets)
        
        gate_a = self.graph.gates[net[0]]
        gate_b = self.graph.gates[net[1]]

        gates = (gate_a, gate_b)

        return net, gates
    
    def remove_net(self, net, gates):
        
        print(f"Net: {net}")
        
        net_path = self.wire_path[net]
        print(f"Net path: {net_path}")
        
        coord_storage = []
        for coordinates in net_path:    
            # Remove old path coordinates from the coordinate storage of the Wire Object
            # Gates can never be an intersection and thus will not be taken into account
            node = self.graph.nodes[coordinates]
            print(f"Node = {node}")
            print(f"Type = {type(node)}")
            if not node.isgate:
                print(f"coordinates: {coordinates}")
                print(f"wire coords: {self.wire.coords}")
                print(f"test")
                
                # Remove node form coordinate storage
                self.wire.coords.remove(node)

                # Correct intersection-count of the Node object of the current coordinate
                node.decrement_intersection()
                
                # Keep track of wire-units in old path
                coord_storage.append(coordinates)
                
                # Create wire unit
                if len(coord_storage) == 2:
                    # Remove old wire units from the path storage of the Wire Object
                    self.wire.path.remove((coord_storage[0], coord_storage[1]))
                    coord_storage.pop(0)


    def apply_random_adjustment(self, net, gates):
        gate_a, gate_b = gates
        new_path = self.make_connection(gate_a, gate_b)
        
        # Update wire_path
        self.wire_path[net] = new_path




    
    
    
    def run(self):
        
        # 1. Initialize a random start state
        # self.get_random_startState()

        # 2. Repeat until cost does not improve after N iterations:
        while self.no_improvement_count < 1000:

            # 3. Apply random adjustment
            # Get random net
            net, gates = self.get_random_net()

            # Remove old net form wire object
            self.remove_net(net, gates)

            # Apply random adjustment on net
            self.apply_random_adjustment(net, gates)
            
            break
            # pass

            # 4. If state worsened (cost increased):

                # 5. Undo adjustment

        