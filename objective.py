from .entity import Position





class Objective:

    
    def __init__(entity, objtype, en_ships):
        self.entity = entity
        self.objtype = objtype
        
        self.my_ships = []
        self.en_ships = []
        updatePriority()
    

    def updatePriority():
        self.priority = 0    
    
    def addMyShip(ship):
        self.my_ships += ship
        updatePriority()
        
    def addEnShip(ship):
        self.en_ships += ship
        updatePriority()

    def remMyShip(ship):
        self.my_ships.remove(ship)
        updatePriority()

