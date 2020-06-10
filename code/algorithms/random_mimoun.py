def generate_path(self):
    """Returns generated wire path."""

    current_path = set()

    # Iterate over connections in netlist
    for connection in self.connections:

        for i in range(self.connections[connection]):

            path = set()

            # Get gateID's
            a, b = connection, self.connections[connection][i]

            # Get gate coordinates
            a_x, a_y = self.gates[a].xcoord, self.gates[a].ycoord
            b_x, b_y = self.gates[b].xcoord, self.gates[b].ycoord

            # Compute steps en difference for x and y
            x_steps = abs(b_x - a_x)
            x_diff = b_x - a_x
            y_steps = abs(b_y - a_y)
            y_diff = b_y - a_y

            x_current = a_x
            y_current = a_y

            x_update = a_x
            y_update = a_y


            # Update and append step coordinates
            while b_x != x_current and b_y != y_current:
                
                # Create options going east, west, north and south
                option_e_coords = (b_x + 1, b_y)
                option_w_coords = (b_x - 1, b_y)
                option_n_coords = (b_x, b_y + 1)
                option_s_coords = (b_x, b_y - 1)

                direction_options = [option_e_coords, option_w_coords, option_n_coords, option_s_coords]

                # Calculate possible collisions
                # Syrka: Hier vind je geen collisions mee, want je checkt alleen coordinaten, dus je kan hier wel
                # intersections mee checken maar voor een collision heb je een a-coordinaat (vertrekpunt) en een
                # b-coordinaat nodig (aankomst punt). Als je deze dan gezamelijk (in een lijst van tuples bv) opslaat, 
                # dan kun je collisions checken
                for option in direction_options:
                    if option in path:
                        direction_options.pop(option)
                
                # If no options
                if len(direction_options) == 0:
                    pass
                    ## Mimoun: Wat als er geen opties zijn?
                    # Syrka: Misschien een volledige restart of een stap terug waarbij je de huidige stap uitsluit als mogelijke optie?

                # If one option
                elif len(direction_options) == 1:
                    optimal_direction = direction_options[1]
                
                # If multiple options left, calculate closest option according to Manhatten distance
                elif len(direction_options) > 1:
                    direction_lengths = {}
                    for option in direction_options:
                        direction_lengths[option] = distance.cityblock([option[0], option[1]], [b_x, b_y])
                    optimal_direction = 0
                    for option in direction_options:
                        if direction_lengths[option] < optimal_direction:
                            optimal_direction = option


                # Generate new wire line
                current_coords = (x_current, y_current)
                x_update = optimal_direction(0)
                y_update = optimal_direction(1)
                step_coords = (x_update, a_y)

                # Only add new wire line if no collision occurs
                ## Mimoun: Waarom checken we hier ook nog 'current_coords'? Als het goed is zit die sowieso al in path toch?
                #  Syr: is deze niet voor het checken van collisions? Want je checkt (vertrekpunt, aankomstpunt) en dat is een wire-unit-length...
                # ...dus eignenlijk houden we hier dan al rekening met de hard constraint van de collisions
                ## Mimoun: Maar als current_coords en step_coords in path staan, betekent dat nog niet dat er collision is, toch?
            #    if (current_coords, step_coords) not in path:
            #        path.add(step_coords)
            #        x_current = x_update

                if b_x == x_update:
                    print('x = check')
                            # Update and append step coordinates
                if b_y == y_update:
                    print('y = check')


    return total_path 