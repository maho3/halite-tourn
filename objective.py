class Objective:

    
    def __init__(self,entity, objtype):
        self.entity = entity
        self.objtype = objtype
        
        self.my_ships = []
        self.en_ships = []
        self.updatePriority()
    

    def updatePriority(self):
        self.priority = 0    
    
    def addMyShip(self,ship):
        self.my_ships.append(ship)
        self.updatePriority()
        
    def addEnShip(self,ship):
        self.en_ships.append(ship)
        self.updatePriority()

    def remMyShip(self,ship):
        self.my_ships.remove(ship)
        self.updatePriority()

