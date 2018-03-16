import hlt
class Objective:

    def __init__(self,entity, objtype):
        self.entity = entity
        self.objtype = objtype
        
        self.my_ships = []
        self.en_ships = []
        self.updatePriority()
    
    def updatePriority(self):
        msc = len(self.my_ships)
        esc = len(self.en_ships)
        enemyUndocked = esc
        myUndocked = msc
        mySpaces = 0
        if type(self.entity) == hlt.entity.Planet:
            dockedShips = len(self.entity.all_docked_ships()) 
            numSpots = self.entity.num_docking_spots
            mySpaces = numSpots - dockedShips
            if self.objtype == 'attack':
                enemyUndocked -= dockedShips 
        
        if self.objtype == 'attack':
            self.priority = 70 + myUndocked * 10 - enemyUndocked * 10             
        elif type(self.entity) == hlt.entity.Planet and self.entity.remaining_resources == 0:
            self.priority = -float('inf')
        elif self.objtype == 'defend':
            if enemyUndocked == 0:
                self.priority = -float('inf')
            else:
                self.priority = 15 * (enemyUndocked - myUndocked)
        elif self.objtype == 'dock_owned' or self.objtype == 'dock_unowned':
            self.priority = 30 - enemyUndocked * 30
            if myUndocked > mySpaces:
                self.priority = -float('inf')
    
    def addMyShip(self,ship):
        self.my_ships.append(ship)
        self.updatePriority()
        
    def addEnShip(self,ship):
        self.en_ships += ship
        self.updatePriority()

    def remMyShip(self,ship):
        self.my_ships.remove(ship)
        self.updatePriority()

