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


class Gate():
    """
    Represents a gate on the grid.
    """

    def __init__(self, gateID, xcoord, ycoord):
        """
        Initialize Gate object.

        Parameters
        ----------
        gateID: an int
                Gate ID.

        xcoord: an int
                The x-coordinate of the gate.

        ycoord: an int
                The y-coordinate of the gate.
        """

        self.gateID = gateID
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = 0

    def __repr__(self):
        """
        Ensure that the object is printed properly if it is in a list/dict.
        
        Return
        ------
        string
                The gate ID.
        """

        return str(self.gateID)

