#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
from collections import Counter

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'


class Wire():
    """
    Represents wire of the chip.
    """

    def __init__(self):
        """
        Initializes a Wire object.
        """

        # Keeps track of wire path for checking on collisions and computing costs
        self.path = set() 

        # Keeps track of coordinates for counting itersections
        self.coords = []

    def update_path(self, position, step):
        """
        Updates the wire path.

        Parameters
        ---------
        position: a Node object
                A node object representing the current position of the wire in the grid.

        step: a Node object
                A node object representing the next position of the wire in the grid.
        """

        # Get position and step coordinates
        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord

        # Sort and convert to tuple to ensure consistent order
        path = tuple(sorted((position_coords, step_coords)))
        self.path.add(path)

    def update_coords(self, position):
        """
        Updates the wire coordinates.
        
        Only append nodes that are not a gate, since intersetions cannot occur on a
        gate Node.
        
        Parameters
        ----------
        position: a Node object
                A node object representing the current position of the wire in the grid.
        """

        if position.isgate is False:
            self.coords.append(position)

    def check_collision(self, position, step):
        """
        Returns True if no collision occurs, otherwise False.
        
        Parameters
        ----------
        position: a Node object
                A node object representing the current position of the wire in the grid.

        step: a Node object
                A node object representing the next position of the wire in the grid.

        Returns
        -------
        bool
                True if successful, otherwise False.
    
        """

        # Get position and step coordinates
        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords = step.xcoord, step.ycoord, step.zcoord

        # Sort and convert to tuple to ensure consistent order
        step = tuple(sorted((position_coords, step_coords)))

        return step not in self.path

    def compute_length(self):
        """
        Returns the length of the wire.

        Returns
        -------
        int
                The length of the wire.
        """

        return len(self.path)

    def compute_intersections(self):
        """
        Returns the number of intersections.
        
        An intersection occurs when a node, that is not a gate, occurs more than 
        once in the wire. The occurance is decremented by 1, to account for the fact
        that an intersetion only occurs when a coordinate is visitid by the wire more
        than once.

        Returns
        -------
        int 
                Number of intersections of the wire.
        """
        
        # Counts occurences of coordinates
        counter = Counter(self.coords)

        # Count number of intersections
        intersections = 0
        for coordinate in counter:
            if counter[coordinate] > 1:
                intersections += counter[coordinate] - 1

        return intersections

    def compute_costs(self):
        """
        Returns the costs of the wire.

        Returns
        -------
        int
                The total costs of the wire. 
        """

        length = self.compute_length()
        intersections = self.compute_intersections()

        return length + 300 * intersections

    