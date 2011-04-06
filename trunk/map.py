import re,missionwrapper,unit,pygame,random,soldier, building

# This class associates a terrain type with its properties
class MovementTable:
    #table = dict()
    def __init__(self):
        self.table = dict()
        
    # In order to use this class you must call load with a filename for the
    # movement
    def load(self,filename):
        filestream = open(filename)

        charA = 'q'
        idA = 0
        passA = True
        #each line is a unique terrain
        for line in filestream:
            charA,idA,passA = line.split()
            self.table[charA] = (idA,passA)    

# This class wraps and provides methods to work with the terrain and units
class Map:
    instance = None
    
    @staticmethod
    def get():
        if(Map.instance == None):
            Map.instance = Map()
        return Map.instance
    
    def __init__(self, filename=None):
        # This is a dictionary which maps a Player object to a list of units
        self.unitTable = dict()
        # A list of lists which hold characters representing the grid
        self.terrainGrid = []
        # A dictionary which maps an index to a Player object
        self.playerIdMap = dict()
        # A dictionary which maps a Player object to a list of bullets
        self.projectiles = dict()
        # Whether there is a map loaded or not
        self.loaded = False
        
        # A hardcoded target for the units to shoot at, until we have units
        # retrievable in the protocols
        self.target = soldier.Soldier(float(6.0*32),float(7.0*32))
        self.target.image.fill((100,0,0))

        # Constant Stuff
        self.tileImage = 'images/tileset.PNG'
        self.width = 800
        self.height = 800
        self.tileSet = pygame.image.load(self.tileImage).convert()
        self.movementTable = MovementTable()
        self.movementTable.load('static.txt')
        
        self.colorMap = {0:(0,0,255), 1:(255,0,0), 2:(250,10,0)}
        # End Constant Stuff

    # For the most part just calls its units' update functions
    def update(self, deltaSeconds):
        for player in self.unitTable:
            for e in self.unitTable[player]:
                newBullet = e.update(deltaSeconds)
                if newBullet is not None:
                    if(self.projectiles.get(player) == None):
                        self.projectiles[player] = []
                    self.projectiles[player].append(newBullet)
                e.keep_on_screen(self.width,self.height)
                e.fire_at(self.target)
            
            if(self.projectiles.get(player) == None):
                self.projectiles[player] = []
            for bullet in self.projectiles[player]:
                bullet.update(deltaSeconds)
                
        self.target.update(deltaSeconds)

    # Draws all of the terrain and units to the screen
    def draw(self, screen):
        for i in range(25):
            for j in range(25):
                screen.blit(self.tileSet,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrainGrid[i])[j])*32,0,32,32))
                
        for player in self.unitTable:
            for unit in self.unitTable[player]:
                unit.draw(screen)
            for bullet in self.projectiles[player]:
                bullet.draw(screen)
                
        if(self.selection != []):
            for unit in self.selection:
                unit.drawfocus(screen)
                
        self.target.draw(screen)
                
    # Returns the tile type for the terrain
    def lookup(self,char):
        return int((self.movementTable.table[char])[0])

    # Closes the mission
    def close(self):
        unitTable = dict()
        terrainGrid = []
        unitPlacements = dict()
        self.playerIdMap = dict()

    # Returns whether the mission is loaded or not
    def is_loaded(self):
        return self.loaded

    # Loads a mission from a mission file
    def load(self,filename):
        # If there is a mission loaded already close it
        if(self.is_loaded() == True):
            self.close()           
                
        self.loaded = True
        self.mouseIsDown = False
        self.mouseRect = pygame.Rect(0,0,0,0)
        self.selection = []
        
        # Get stuff from wrapper
        self.wrapper = missionwrapper.Wrapper()
        self.wrapper.load(filename)
        terrainList = self.wrapper.GetMap()
        playerList = self.wrapper.GetPlayer()
        unitList = self.wrapper.GetUnits()
        
        # Initialize the terrain grid
        holder = []
        for line in terrainList:
            for char in line:
                #don't add the trailing newline
                if(char == '\n'):
                    continue
                #append the char to the end of the list 'holder'
                holder[len(holder):] = [char]
            #all chars in 'line' are in holder
            self.terrainGrid.append(holder)
            #set holder to empty
            holder = []

        # Initialize the Player objects
        index = 0
        for player in playerList:
            player.replace('\n','')
            aiA = ""
            strType = ''
            res1 = 1
            res2 = 3
            aiA,strType,res1,res2 = player.split()
            self.playerIdMap[index] = Player()
            self.playerIdMap[index].ai = aiA
            self.playerIdMap[index].type = strType
            self.playerIdMap[index].resource = (res1,res2)
            index = index + 1
        
        # Load in and spawn units
        for units in unitList:
            units.replace('\n','')
            playerObject = self.playerIdMap[0]
            #print self.playerIdMap
            #print playerObject
            #read each individual unit's line
            xA = 1
            yA = 1
            unitId = 1
            playerId = 0
            xA,yA,unitId,playerId = units.split()
            xA = float(xA)
            yA = float(yA)
            unitId = int(unitId)
            playerId = int(playerId)
            if(int(unitId) == 3):
                unitObject = building.Building(xA*32,yA*32)
            else:
                unitObject = soldier.Soldier(xA*32, yA*32, self.colorMap[playerId])
            playerObject = self.playerIdMap[playerId]
            if(self.unitTable.get(playerObject) == None):
                self.unitTable[playerObject] = []
            self.unitTable[playerObject].append(unitObject)
            self.unitPlacements[unitObject] = (xA,yA)
            
    # Checks for unit collision against terrain
    def terrain_collision(self,unit):
        map.Map.get().collision(self)
        too = ((self.terrainGrid[unit.rect.x/32])[unit.rect.y/32])
        if((self.movementTable.table[too])[1]):
            return True
        return False

    # Checks for unit collision against other units
    def unit_collision(self,unit):
        for player in self.unitTable:
            for unitA in self.unitTable[player]:
                if(unitA.rect.colliderect(unit.rect)):
                    return True
        return False

    # Composite of unit_collision and terrain_collision
    def collision(self,unit):
        if(self.terrain_collision(unit)):
            return True
        if(self.unit_collision(unit)):
            return True
        return False

    # Populates the selection, based on what collides with
    # the given rect
    def select_group(self,rect):
        self.selection = []
        
        player = self.playerIdMap[0]
        for unitA in self.unitTable[player]:
            if(unitA.rect.colliderect(rect)):
                self.selection.append(unitA)
    
class Player:
    ai = ""
    type = ""
    resource = (0,0)
    def __init__(self):
        type = ''
