# Chips & Circuits

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

- matplotlib (...<versie>)    
- scipy (...<versie>)    
- numpy (...<versie>)    
....    

### Usage
(...<nog verder in te vullen>)

### Repository
The following list describes the most important files in the project and where to find them:

- /code: contains all of the codebase of this project.
    - /code/algorithms: contains code to run the algorithms.
        - (...<evt nog specifieke algorithm-files weergeven>)
    - /code/classes: contains four classes necessary for the project.
        - (...<evt nog specifieke classes-files weergeven>)
    - /code/visualization: contains code that generates a visualisation of the designed chip(s).
- /gates&netlists: contains multiple datafiles necessary for initialising the chip and graph.

## Authors
- Eline van Groningen
- Mimoun Boulfich
- Syrka van Kuppenveld

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/SyrkavanKuppenveld/progressierups/blob/master/LICENSE) file for details.