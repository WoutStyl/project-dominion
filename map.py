import re,os,missionwrapper,unit,pygame,random,soldier,building,objective, queueitem, menu

# Collaborators:
#   Player
#   Menu
#   Unit
#   MovementTable
#   MissionWrapper
#   Function
# Responsibilities:
#   contains all of the players and their units. passes down the update
#   and draw function calls. holds the current in-game menu as well.

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
        # Objective object list
        self.objectiveList = []
        

        # Constant Stuff
        self.tileImage = 'images/tileset.PNG'
        self.width = 1600
        self.height = 1600
        #the whole 256 x 256 grid in pixels 50 x 50
        self.tileSet = pygame.image.load(self.tileImage).convert()
        self.movementTable = MovementTable()
        self.movementTable.load('static.txt')
        self.view = pygame.Surface((self.width,self.height))
        self.colorMap = {0:(0,0,255), 1:(255,0,0), 2:(250,10,0)}
        # End Constant Stuff
        self.protocols = []
        self.unitMenu = menu.Menu()
        self.unitMenu.leave_menu()
        self.selection = []
        self.newSelection = True

    # For the most part just calls its units' update functions
    def update(self, deltaSeconds):
        for player in self.unitTable.keys():
            for e in self.unitTable[player]:
                newBullet = e.update(deltaSeconds)
                if newBullet is not None:
                    if(self.projectiles.get(player) == None):
                        self.projectiles[player] = []
                    self.projectiles[player].append(newBullet)
                e.keep_on_screen(self.width,self.height)
                self.collision(e)
                #print(self.unitTable[self.playerIdMap[1]][0])
            
            if(self.projectiles.get(player) == None):
                self.projectiles[player] = []
            for bullet in self.projectiles[player]:
                bullet.update(deltaSeconds)
                if(self.bullet_collision(bullet, player)):
                    bullet.die();
                    self.projectiles[player].remove(bullet)
                

    # Draws all of the terrain and units to the screen
    def draw(self, screen, upperleft, rect):
        #x = pygame.display.set_mode((self.width,self.height))
        for i in range(50):
            for j in range(50):
                #build everything onto view
                self.view.blit(self.tileSet,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrainGrid[i])[j])*32,0,32,32))
                #screen.blit(self.tileSet,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrainGrid[i])[j])*32,0,32,32))
                #x.blit(self.tileSet,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrainGrid[i])[j])*32,0,32,32))
        #for i in range(25):
            #for j in range(25):
        #screen.blit(x,(0,0),pygame.Rect(upperleft[0],upperleft[1],32*25,32*25))
        #screen.blit(self.view,(0,0),pygame.Rect(upperleft[0],upperleft[1],32*25,32*25))
        for player in self.unitTable.keys():
            for unit in self.unitTable[player]:
                unit.draw(self.view)
            if(len(self.projectiles[player]) > 0):
                for bullet in self.projectiles[player]:
                    bullet.draw(self.view)
                
        pygame.draw.rect(self.view,(175,175,175),rect,2)
        screen.blit(self.view,(0,0),pygame.Rect(upperleft[0],upperleft[1],32*25,32*25))
        queue = self.get_unit_queue()
        for u in queue:
            u.draw(screen)
    def get_unit_menu(self):
        return self.unitMenu
    def get_unit_queue(self):
        if len(self.selection) == 1 and self.selection[0].get_type() == "Building":
            return self.selection[0].get_unit_queue()
        return []
    # Returns the tile type for the terrain
    def lookup(self,char):
        return int((self.movementTable.table[char])[0])

    # Closes the mission
    def close(self):
        self.unitTable = dict()
        self.terrainGrid = []
        self.playerIdMap = dict()

    # Returns whether the mission is loaded or not
    def is_loaded(self):
        return self.loaded

    def drawmouse(self,screen,rect,upperleft):
        pygame.draw.rect(self.view,(175,175,175),rect,2)
        screen.blit(self.view,(0,0),pygame.Rect(upperleft[0],upperleft[1],32*25,32*25))

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
        objectiveList = self.wrapper.GetObjective()

        #Construct the list of Objectives
        for objtive in objectiveList:
            self.objectiveList.append(objective.Objective(objtive))
        
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
            if(unitId == 3):
                unitObject = building.Building(self.playerIdMap[playerId], xA*32,yA*32, self.colorMap[playerId])
            else:
                unitObject = soldier.Soldier(xA*32, yA*32, None, self.colorMap[playerId])
            playerObject = self.playerIdMap[playerId]
            if(self.unitTable.get(playerObject) == None):
                self.unitTable[playerObject] = []
            self.unitTable[playerObject].append(unitObject)
    # Checks for bullet collision against enemies
    def bullet_collision(self, bullet, player1):
        for player in self.unitTable.keys():
            if player != player1:
                for unitA in self.unitTable[player]:
                    if(unitA.rect.colliderect(bullet.rect)):
                        #print("HIT");
                        unitA.take_damage(5)
                        if unitA.is_dead():
                            #return True
                            self.unitTable[player].remove(unitA)
                        return True
        return False
        
    # Checks for unit collision against terrain
    def terrain_collision(self,unit):
        pos = unit.get_pos()
        rect = pygame.Rect(int(pos[0]/32*32),int(pos[0]/32*32),32,32)
        too = self.terrainGrid[int(pos[0]/32)][int(pos[1]/32)]
        value = self.movementTable.table[too][1]
        return unit.collide_terrain(rect, value)

    # Checks for unit collision against other units
    def unit_collision(self,unit):
        for player in self.unitTable.keys():
            for unitA in self.unitTable[player]:
                if unit.collide_unit(unitA):
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
        #self.newSelection = True
        for unit in self.selection:
            unit.set_selected(False);
            
        self.selection = []
        
        player = self.playerIdMap[0]
        for unitA in self.unitTable[player]:
            if(unitA.rect.colliderect(rect)):
                self.selection.append(unitA)
                unitA.set_selected(True)
                
        if(self.selection != []): #and self.newSelection is True:
            if len(self.selection) == 1 and self.selection[0].unitMenu == "Build":
                self.unitMenu = menu.BuildMenu(self.selection[0])
                return
            for unit in self.selection:
                if unit.unitMenu == "Standard":
                    #self.newSelection = False
                    self.unitMenu = menu.UnitMenu()
                    return
            #self.newSelection = False
        self.unitMenu = menu.Menu()
        self.unitMenu.leave_menu()
        return
                
    # Saves the current state of the world to the filename
    def save(self,path=None):
        if path != None:
            filename = os.path.split(self.wrapper.GetName())[1]
            filename = os.path.join(path, filename)
            self.wrapper.SetName(filename)
        
        unitOutput = []
        playerOutput = []
        for i in range(len(self.unitTable)):
            playerObj = self.playerIdMap[i]
            for unit in self.unitTable[playerObj]:
                id = 0
                if unit.get_type() == "Building":
                    id = 3
                unitOutput.append(self.wrapper.FormatUnit(unit,i,id))
            line = playerObj.ai + ' ' + playerObj.type + ' ' + playerObj.resource[0] + ' ' + playerObj.resource[1]
            playerOutput.append(line)
        self.wrapper.SetMap(self.terrainGrid)
        self.wrapper.SetPlayer(playerOutput)
        self.wrapper.SetUnits(unitOutput)
        self.wrapper.save()
        
    def spawn_unit(self, player, unit):
        for id in self.playerIdMap.keys():
            if self.playerIdMap[id] == player:
                color = self.colorMap[id]
                
        unit.set_color(color)
        self.unitTable[player].append(unit)
        
        
    def add_new_protocol(self, p):
        self.protocols.append(p)
        
    def set_protocol_by_index(self, p, i):
        self.protocols.insert(i, p)
        self.protocols.pop(i+1)
        
    def remove_protocol_by_index(self, i):
        self.protocols.pop(i)

    def set_protocol_for_selection(self, i):
        for u in self.selection:
            u.set_protocol(self.protocols[i])
            
    def get_an_enemy_unit(self, aUnit, args):
        thePlayer = None
        for player in self.unitTable.keys():
            for unit in self.unitTable[player]:
                if unit == aUnit:
                    thePlayer = player
                    break
        for player in self.unitTable.keys():
            if player != thePlayer and len(self.unitTable[player]) != 0:
                return self.unitTable[player][0]
        return None
        
 
class Player:
    ai = ""
    type = ""
    resource = (0,0)
    def __init__(self):
        type = ''
