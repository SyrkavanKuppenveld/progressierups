#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'

"""
Code for the Node class.


This module contains the code for the Node class. 
"""


class Node():
    """
    Creates a Node object which represents a coordinate on the grid.
    """

    def __init__(self, coords):
        """
        Initializes a Node object.
        
        Parameters
        ----------
        coords: a tuple
                A tuple containing the x-, y- and z-coordates of the grid.
        """

        self.xcoord = coords[0]
        self.ycoord = coords[1]
        self.zcoord = coords[2]
        self.neighbors = set()
        self.isgate = False
        self.intersection = 0

    def add_neighbor(self, neighbor):
        """
        Appends neighbor to neighbors.

        Parameters
        ----------
        neighbor: a Node object 
                A Node object representing the neighbor of the current position of the wire.
        """

        self.neighbors.add(neighbor)

    def set_isgate(self):
        """
        Set self.isgate to True.
        """

        self.isgate = True

    def increment_intersection(self):
        """
        Increments self.intersection with 1.
        """

        self.intersection += 1

    def decrement_intersection(self):
        """
        Decrements self.intersection with 1.
        """

        self.intersection -= 1

    def get_copy(self):
        """
        Returns a "deep" copy of the Node.
        
        Returns
        -------
        Node object
                A 'deep' copy of the Node object.
        """

        # Instantiate new node object with same coordinates
        copy = Node((self.xcoord, self.ycoord, self.zcoord))

        # Set all attributes equal to self
        copy.neighbors = self.neighbors
        copy.isgate = self.isgate
        copy.intersection = self.intersection
        
        return copy

    def get_resursive_wire_density(self, node, surroundingWires, wirePath, count, radius):
        """
        Recursively looks at all neighbors within a given radius of the initial node 
        and check how many wire-units are encountered on the way.

        Parameters
        ----------
        node : a Node object
                A Node Object whose directions are checked on having a path laid upon them.

        surroundingWires : an int
                A number representing the number of wire units encounters thus far.

        wirePath : a set
                A set of tuples representing the wire units laid by the algorithm (thus far).

        count : an int
                An integers that keeps track of the recursion depth.

        radius : an int
                An integer that specifies the depth of the recursion.

        Returns
        -------
        list
                A list of which the number of elements represent the number of wires 
                encountered thusfar.

        """

        # Recurisively get the number of wire units within radius distance
        if count < radius:
            count += 1

            # For each neighbor of the current node
            for neighbor in node.neighbors:
                neighborCoords = (neighbor.xcoord, neighbor.ycoord, neighbor.zcoord)
                currentNodeCoords = (node.xcoord, node.ycoord, node.zcoord)
                
                # Check if a wire path has been placed on the path to the current neighbor 
                wireToNeighbor = tuple(sorted((currentNodeCoords, neighborCoords))) 
                if wireToNeighbor in wirePath:
                    surroundingWires.append(1)
                    return surroundingWires
                
                # Update the node and resume recursion
                node = neighbor
                self.get_resursive_wire_density(node, surroundingWires, wirePath, count, radius)
        
        return surroundingWires
    
    def get_wire_density(self, initialNode, wirePath):
        """
        Retrieves the number of wire lengths within a pre-specified radius surrounding the 
        current neihbour in a pre-specified radius.

        Parameters
        ----------
        initialNode : a Node object
                A Node object representing the current Node
        wirePath : set
                A set af coordinate-combinations representing the wire-length units 
                of the path laid thusfar

        Returns
        -------
        int
                The number of wires surrounding the current node
        """
        
        node = initialNode
        surroundingWires = []
        
        # Determine radius (recursion depth)
        count = 0
        radius = 2
        
        # Get the number of surrounding wires
        surroundingWires = self.get_resursive_wire_density(node, surroundingWires, wirePath, count, radius)

        return len(surroundingWires)
    
    def __repr__(self):
        """Ensure that the object is printed properly if it is in a list/dict.
        
        Returns
        -------
        str
                The coordinates of the Node object.
        """

        return str((self.xcoord, self.ycoord, self.zcoord))

    

    

    



    
