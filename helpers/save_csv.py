import csv
import re

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
    writer.writerow([f'chip_{chip}_net_{net}', costs])

    print("For output see: 'output.csv'.")