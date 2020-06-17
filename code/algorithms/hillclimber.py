from code.classes import Graph
from code.algorithms import Greedy_RandomNet_LookAhead, Greedy_RandomNet
from code.visualization import Chip_Visualization
import random

class HillClimber(Greedy_RandomNet_LookAhead):
    """
    <INFORMATIE>
    """

    def __init__(self, random_startState, start_wire_path, start_cost):
        """ 
        Initializes the start state of the algorithm.
        """
    
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
        return net
    
    def remove_net(self, net):
        pass


    def apply_random_adjustment(self, net):
        gate_a, gate_b = net
        
        new_path = self.make_connection(gate_a, gate_b)
        self.wire_path[net] = new_path




    
    
    
    def run(self):
        
        # 1. Initialize a random start state
        # self.get_random_startState()

        # 2. Repeat until cost does not improve after N iterations:
        while self.no_improvement_count < 1000:

            # 3. Apply random adjustment
            # Get random net
            net = self.get_random_net()

            # Remove old net form wire
            self.remove_net(net)

            # Apply random adjustment on net
            self.apply_random_adjustment(net)
            
            break
            # pass

            # 4. If state worsened (cost increased):

                # 5. Undo adjustment

        