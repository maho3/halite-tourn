import hlt
import logging
import micro
from objective import Objective

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

# objtype = ['attack','defend','dock_owned', 'dock_unowned']
def updateObjectives(game_map, opponent_ships):
    objs = []
    for p in planets:
        en_list = sorted(opponent_ships, key=lambda x: p.calculate_distance_between(x)) 
        for i in range(len(en_list)):
            if p.calculate_distance_between(en_list[i]) > 40 - p.radius:
                break
        
        if not p.is_owned() and p.remaining_resources > 0:
            objs.append(Objective(p, 'dock_unowned'))
            objs[-1].addEnShip(en_list[:i])
        elif p.owner == me:
            objs.append(Objective(p, 'defend'))
            objs[-1].addEnShip(en_list[:i])
            if not p.is_full() and p.remaining_resources > 0:
                objs.append(Objective(p,'dock_owned'))
                objs[-1].addEnShip(en_list[:i])
        elif p.owner != me and p.is_owned():
            objs.append(Objective(p, 'attack'))
            objs[-1].addEnShip(en_list[:i])
            
        
    return objs

def assignObjectives(objectives, my_ships):
    if len(objectives) == 0:
        return objectives
    for ship in my_ships:
        if (ship.docking_status == 1 or ship.docking_status ==2) and ship.planet.remaining_resources > 0:
            continue
        bestObj = objectives[0]
        bestScore = -100000
        for obj in objectives:
            score = obj.priority - ship.calculate_distance_between(obj.entity) * 2
            if score > bestScore:
                bestScore = score
                bestObj = obj
        bestObj.addMyShip(ship)
        logging.info('i am at ' + str(ship.x) + ' ' + str(ship.y) + ' my obj is to ' + str(bestObj.objtype) + ' at ' + str(bestObj.entity.x) + ' ' + str(bestObj.entity.y) + ' against ' + str(len(bestObj.en_ships)) + ' ships')
    return objectives

#flee_pos = [hlt.entity.Position(0,0), hlt.entity.Position(game_map.width-1,0),
#                    hlt.entity.Position(0,game_map.height-1),
#                    hlt.entity.Position(game_map.width-1,game_map.height-1)]
def flee(game_map):
    for ship in my_ships:
        navigate_command = None
        if (ship.docking_status != ship.DockingStatus.UNDOCKED):
            navigate_command = ship.undock()
        else:
            if (ship.y <= 5) and (ship.x > 5):
                flee_pos = hlt.entity.Position(0,3)
            elif (ship.x <= 5) and (ship.y < game_map.height - 5):
                flee_pos = hlt.entity.Position(3,game_map.height)
            elif (ship.y >= game_map.height - 5) and (ship.x < game_map.width - 5):
                flee_pos = hlt.entity.Position(game_map.width, game_map.height - 3)
            elif (ship.x >= game_map.width - 5) and (ship.y > 5):
                flee_pos = hlt.entity.Position(game_map.width - 3, 0)
            else:
                flee_pos = min( hlt.entity.Position(ship.x, 0),
                                hlt.entity.Position(0, ship.y),
                                hlt.entity.Position(ship.x, game_map.height),
                                hlt.entity.Position(game_map.width, ship.y),
                                key = lambda p: ship.calculate_distance_between(p))
            
            navigate_command = ship.navigate(flee_pos, 
                                            game_map,
                                            speed=int(hlt.constants.MAX_SPEED),
                                            entities=own_ships_nav)
            
        if navigate_command is not None:
            command_queue.append(navigate_command)
            
    return command_queue



me = None
turn = 0

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    turn+=1
    logging.info(str(turn))
    game_map = game.update_map()
    me = game_map.get_me()
    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    
    own_ships_nav = [] #list of our ships by position just for navigation purposes
    command_queue = []
    planets = game_map.all_planets()
    opponent_ships = []
    my_ships = game_map.get_me().all_ships()
    
    for player in game_map.all_players():
        if player.id != game_map.get_me().id:
            opponent_ships += player.all_ships()
    
    if (0.95*len(my_ships) < 0.1*len(opponent_ships)):
        command_queue = flee(game_map)
        game.send_command_queue(command_queue)
        continue
    
    
    objectives = updateObjectives(game_map, opponent_ships)
    
    objectives = assignObjectives(objectives, my_ships)

    for objective in objectives:
        command_queue += micro.getMovesForObjective(objective, game_map, own_ships_nav, opponent_ships)

    
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
                    speed=int(hlt.constants.MAX_SPEED), entities=own_ships_nav)
            
            if (navigate_command != None):
                command_queue.append(navigate_command)
            break
    
    ''' 
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END

# GAME END
