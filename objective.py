from .entity import Position





class Objective:

    
    def __init__(entity, objtype, my_dock, my_spaces):
        self.entity = entity
        self.objtype = objtype
        self.my_dock = my_dock
        self.my_spaces = my_spaces
        
        self.my_ships = []
        self.en_ships = []
        
    
    def updatePriority():
        return 0
        
    
    def addMyShip(ship):
        self.my_ships += ship
        updatePriority()
    def addEnShip(ship):
        self.en_ships += ship
        updatePriority()
    def remMyShip(ship):
        self.my_ships.remove(ship)
        updatePriority()

