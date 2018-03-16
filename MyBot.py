import hlt
import logging
import objective
import micro
import ship

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Version2")
# Then we print our start message to the logs
logging.info("Starting my Version2 bot!")
'''
def attack_docked_ships(ship, planet, own_ships, game_map):
    docked_ships = planet.all_docked_ships()
    for opponent_ship in docked_ships:
        navigate_command = ship.navigate(ship.closest_point_to(opponent_ship, min_distance=0), game_map, speed=int(hlt.constants.MAX_SPEED), entities=own_ships)
    
        #if you can't attack nearest ship just return None
        return navigate_command

    return None

def attack_ships(ship, entities_by_distance, own_ships, game_map):
    for ship_distance in sorted(entities_by_distance):
        nearest_ship = next((nearest_entity for nearest_entity in entities_by_distance[ship_distance] if isinstance(nearest_entity, hlt.entity.Ship)), None)
        
        if nearest_ship == None:
            continue
        if nearest_ship.owner==game_map.get_me():
            continue
        navigate_command = ship.navigate(ship.closest_point_to(nearest_ship, min_distance=0), game_map, speed=int(hlt.constants.MAX_SPEED), entities=own_ships)
        return navigate_command
    return None
'''

def updateObjectives(game_map):
    return []

def assignObjectives(objectives, shipToObjective, game_map):
    return {}

def getMovesForObjective(objective):
    return {}

objectives = []
shipToObjective = {}
while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    own_ships = []
    command_queue = []
    
    objectives = updateObjectives(game_map)
    shipToObjective = assignObjectives(objectives, shipToObjective, game_map)

    for objective in objectives:
        command_queue += getMovesForObjective(objective)

    
    ''' 
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue
    
        
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        nearest_planet = None

        if len(game_map.all_players()) == 2:
            navigate_command = attack_ships(ship, entities_by_distance, own_ships, game_map)
            
            if (navigate_command != None):
                command_queue.append(navigate_command)
                continue

        for distance in sorted(entities_by_distance):
            nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance] if isinstance(nearest_entity, hlt.entity.Planet)), None)
            
            if nearest_planet == None:
                continue

            navigate_command = None
            #if nearest planet is opponents, attack the docked ships there
            if nearest_planet.is_owned() and nearest_planet.owner!=game_map.get_me():
                navigate_command = attack_docked_ships(ship, nearest_planet, own_ships, game_map)
            
            # If we can dock at a planet, let's (try to) dock. If two ships try to dock at once, neither will be able to.
            elif ship.can_dock(nearest_planet) and not (nearest_planet.is_full()):
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(nearest_planet))
            
            elif nearest_planet.owner==game_map.get_me():
                #if we can't doc and it is our planet, just continue
                continue
            
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(nearest_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED), entities=own_ships)
            
            if (navigate_command != None):
                command_queue.append(navigate_command)
            break
    
    ''' 
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END

# GAME END
