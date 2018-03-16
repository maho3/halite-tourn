def getMovesForObjective(objective, game_map, own_ships_nav):
    commands = []
    for ship in objective.my_ships:
        command = navigate(navigate_command = ship.navigate(
                                                ship.closest_point_to(objective.entity),
                                                game_map,
                                                speed=int(hlt.constants.MAX_SPEED),
                                                entities=own_ships_nav)
        if (command != None):
            commands.append(command)
    return commands
                           

