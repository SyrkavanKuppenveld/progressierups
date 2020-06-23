#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import csv
import re

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'

"""
Save output.csv for check50.


This module contains the code for saving the algorithm output in a csv
file according to the correct check50 layout. 
"""



def save_csv(netlist_file, outfile, wire_path, costs):
    """
    Output a CSV file containing the wire path per connection.

    Parameters 
    ----------     
    netlist_file: a csv file
            Name of the csv file containing a netlist.

    outfile: a csv file
            A plain csv file for the output.

    wire_path: dict
            A dictionary containing the wire path per connection. 

    Output
    ------
    csv file
            A csv file containing the connections and the wire_path. 
            In the correct format for the check50.
    """

    # Generate chip and netlist number 
    plain = re.sub("[^0-9]", "", netlist_file)
    chip = plain[0]
    net = plain[1]

    # Initialize csv write object
    writer = csv.writer(outfile)

    # Write headers
    writer.writerow(['net', 'wires'])

    # Write rows for connection and wire path in correct format for check50
    for connection in wire_path:
        layout = ""
        for i, coordinate in enumerate(wire_path[connection]):
            if i == 0:
                layout += (f'([{coordinate[0]},{coordinate[1]},{coordinate[2]}),')
            elif i == len(wire_path[connection]) - 1:
                layout += (f'({coordinate[0]},{coordinate[1]},{coordinate[2]})]')
            else:
                layout += (f'({coordinate[0]},{coordinate[1]},{coordinate[2]}),')

        # Write row for connection and corresponding wire path
        writer.writerow([f"({connection[0]},{connection[1]})", f"{layout}"])

    # Write row with chip and netlist information
    writer.writerow([f"chip_{chip}_net_{net}", costs])

    print("\033[34m""For output see: 'output.csv'.""\033[0m")