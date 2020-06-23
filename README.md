# Chips & Circuits

<img src="https://thebossmagazine.com/wp-content/uploads/2017/08/microchip-stylized-header-image.jpg" width="251" height="167" />

Chips (or: integrated circuits) are found in various places in our everyday life including our PC, MacBook, Android Phone and microwave oven.

A chip is made up of a small plate of silicon, an is usually designed logically and subsequentially transformed to a list of connectable gates (= netlist). This netlist, is finally transformed into a 2-dimensional design on a silicon base. The last step of connecting the gates, is highly volatile. Good arrangements with short nets lead to faster circuits, whereas poor arrangements with long nets lead to slower circuits. Besides, shorter nets are cheaper than long nets. So, a good arrangement of logical gates and short nets between them is of vital importance, both economically and performancewise.

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

**Possible Choices**    
_Chip_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_Netlist_    
Chip 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 1    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 2    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 3    

Chip 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 4    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 5    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 6    

Chip 2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 7    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 8    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Netlist 9    

_Algorithm_
- Random    
    Korte uitleg...
- Greedy    
    Korte uitleg...
- Greedy Look Ahead    
    Korte uitleg...
- Hillclimber    
    Korte uitleg...
- Restart Hillclimber    
    Korte uitleg...

_Heuristics_
- Social Map    
    Korte uitleg...    
- Better A Neighbor Who Is Near Than A Brother Far Away?    
    Korte uitleg...    
- Sky Is The Limit    
    Korte uitleg...    
- Wire Can’t Touch This    
    Korte uitleg...    
- Wire Jam    
    Korte uitleg...    

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
    - /code/visualization: contains code that generates a visualisation of the designed chip and wire.
- /gates&netlists: contains multiple datafiles needed for initialization of the chip and connections.

## Authors
- Eline van Groningen
- Mimoun Boulfich
- Syrka van Kuppenveld

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE v3 - see the [LICENSE](https://github.com/SyrkavanKuppenveld/progressierups/blob/master/LICENSE) file for details.