import hlt

def weak_ship(planet):
    return planet.all_docked_ships()[0]

def get_nearest_enemy_ship(planet, opponent_ships):
    current_dist = None
    nearest_ship = None
    for ship in opponent_ships:
        if current_dist == None:
            current_dist = ship.calculate_distance_between(planet)
            nearest_ship = ship
        if ship.calculate_distance_between(planet) < current_dist:
            current_dist = ship.calculate_distance_between(planet)
            nearest_ship = ship
    return hlt.entity.Position((nearest_ship.x + planet.x)/2, (nearest_ship.y + planet.y)/2)

def getMovesForObjective(objective, game_map, own_ships_nav, opponent_ships):
    commands = []
    target = None
    if objective.objtype == 'dock_unowned' or objective.objtype == 'dock_owned':
        target = objective.entity
    elif objective.objtype == 'defend':
        # target = get_nearest_enemy_ship(objective.entity, opponent_ships)
        if len(objective.en_ships) == 0:
            target=None
        else:
            nearest_ship = objective.en_ships[0]
            if nearest_ship.calculate_distance_between(objective.entity) <= 2*objective.entity.radius:
                target = nearest_ship.closest_point_to(objective.entity)
            else:
                target = hlt.entity.Position((nearest_ship.x + planet.x)/2, (nearest_ship.y + planet.y)/2)
    elif objective.objtype == 'attack':
        target = weak_ship(objective.entity)
    
    if target != None:
        for ship in objective.my_ships:
            command = None
            if ship.docking_status == 2 or ship.docking_status == 3:
                command = ship.undock()
            elif (objective.objtype == 'dock_owned' or objective.objtype == 'dock_unowned')  and ship.can_dock(objective.entity) and not objective.entity.is_full():
                command = ship.dock(objective.entity)
            else:
                command = ship.navigate(
                                        ship.closest_point_to(target),
                                        game_map,
                                        speed=int(hlt.constants.MAX_SPEED),
                                        entities=own_ships_nav)
            if (command != None):
                commands.append(command)
    return commands
                           

