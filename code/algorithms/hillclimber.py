from code.algorithms import Greedy_RandomNet
from code.algorithms import Greedy_RandomNet_LookAhead

class HillClimber():
    """
    <INFORMATIE>
    """

    def __init__(self, wire_path):
        """ 
        Initializes the start state of the algorithm.
        """
    
        self.startState = wire_path
        print(self.startState)