"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Version2")
# Then we print our start message to the logs
logging.info("Starting my Version2 bot!")

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


while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()


    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    own_ships = []
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
                # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                # We run this navigate command each turn until we arrive to get the latest move.
                # Here we move at half our maximum speed to better control the ships
                # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                # This will mean that you have a higher probability of crashing into ships, but it also means you will
                # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                # wish to turn that option off.
                navigate_command = ship.navigate(
                    ship.closest_point_to(nearest_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED), entities=own_ships)
                
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
            if (navigate_command != None):
                command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
