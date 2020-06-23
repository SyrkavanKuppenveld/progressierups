# Chips & Circuits

<img src="https://thebossmagazine.com/wp-content/uploads/2017/08/microchip-stylized-header-image.jpg" width="251" height="167" />

Chips (or: integrated circuits) are found in various places in our everyday life including our PC, MacBook, Android Phone and microwave oven.

A chip is made up of a small plate of silicon, and is usually designed logically and subsequentially transformed to a list of connectable gates (= netlist). This netlist, is finally transformed into a 2-dimensional design on a silicon base. The last step of connecting the gates, is highly volatile. Good arrangements with short nets lead to faster circuits, whereas poor arrangements with long nets lead to slower circuits. Besides, shorter nets are cheaper than long nets. So, a good arrangement of logical gates and short nets between them is of vital importance, both economically and performancewise.

We are provided with chips and netlists and it is up to us to find good wiring patterns.

## Getting Started
The code is entirely written in Python 3.7. The instructions below will enable you to get the project up and running on your local machine.

### Prerequisites
Prerequisite libraries, and packages can be installed through:    

`pip install -r requirements.txt`    

or    

`conda install --file requirements.txt`

This will install the correct versions of:
     
- matplotlib (3.2.1)
- numpy (1.18.4)
- pandas (1.0.3)
- seaborn (0.10.1)     

### Usage
Running `python main.py` will start an interactive interface which will ask you which:
- chip
- netlist
- algorithm
- heuristic(s)     
...are to be used.

Subsequently, it will ask whether the solution(s) and/or plot(s) need to be shown and/or saved.
After all choices have been made, the program will start generating a solution.

#### Possible Choices    
*Chip* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Netlist*    
Chip 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 1    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 2    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 3    

Chip 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 4    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 5    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 6    

Chip 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 7    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 8    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 9    

**Short Descriptions**
        
_Algorithms_
- Random
    - The order of the connections is random and the next position of the path is generated randomly.
- Greedy
    - Chooses the step with the lowest Manhattan Distance, if multiple steps with the lowest Manhattan Distance, chooses one of these randomly.
- Greedy LookAhead
    - Inherits functionality from the Greedy algorithm, but also looks 4 steps ahead when chosing a next step. If multiple steps are equally favourable, it chooses one of these randomly.
- Hillclimber
    - Acquires a start state from the Random algorithm and randomly chooses the connection that is to be altered. Builds the new path with an inherited function of the Greedy LookAhead algorithm.
- Restart Hillclimber
    - Runs the Hillclimber multiple times in a row.

_Heuristics_
- Social Map    
    - min: starts building connections of gates that have the fewest gates in their vicinity.
    - max: starts building connections of gates that have the most gates in their vicinity.
- Better A Neighbor Who Is Near Than A Brother Far Away?    
    - min: starts building connections between gates that are closest to each other.
    - max: starts building connections between gates that are furthest away from each other.
- Sky Is The Limit: increases cost when steps are on the bottom 4 layers of the chip.   
- Wire Can’t Touch This: handles intersections as a hard constraint.
- Wire Jam: increases costs of steps that lead to a wire-dense area.

### Repository
The following list describes the most important files in the project and where to find them:

- /code: contains all of the codebase of this project.
    - /code/algorithms: contains code to run the algorithms with.
        - /code/algorithms/greedy.py: contains the Greedy algorithm and extensions thereof.
        - /code/algorithms/hillclimber: contains the HillClimber algorithm.
        - /code/algorithms/random: contains the Random algorithm.
    - /code/classes: contains four classes necessary for the project.
        - /code/classes/gates.py: contains the Gate Class.
        - /code/classes/graph.py: contains the Graph Class.
        - /code/classes/node.py: contains the Node Class.
        - /code/classes/wire.py: contains the Wire Class.
    - /code/visualization: contains code that generates a visualisation of the designed chip.
- /gates&netlists: contains multiple datafiles needed for initialization of the chip and connections.

## Authors
- Eline van Groningen
- Mimoun Boulfich
- Syrka van Kuppenveld

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE 3.0 - see the [LICENSE](https://github.com/SyrkavanKuppenveld/progressierups/blob/master/LICENSE) file for details.