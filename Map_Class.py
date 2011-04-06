import re,Mission_Wrapper,unit,pygame,random,soldier, building

class Movement_Table:
    """
This class associates a terrain type with its properties
    """
    #table = dict()
    def __init__(self):
        self.table = dict()
    def load(self,filename):
        """
In order to use this class
you must call load with a
filename for the movement
        """
        filestream = open(filename)

        char_a = 'q'
        id_a = 0
        pass_a = True
        #each line is a unique terrain
        for line in filestream:
            char_a,id_a,pass_a = line.split()
            self.table[char_a] = (id_a,pass_a)    

class Map:
    """
This class wraps and provides
methods to work with the terrain
and units
unit_table is a dictionary
which maps a Player object to a list of units
terrain_grid is a list of lists (char array array)
this is statically created at mission load
unit_placements is a dictionary
which maps a Unit object to its Location object
    """
    instance = None
    
    @staticmethod
    def get():
        if(Map.instance == None):
            Map.instance = Map()
        return Map.instance
    
    def __init__(self, filename=None):
        """
So when you want to create a new Map object you want to
pass it the filename of the mission you want to load under
the covers it creates a Mission_Wrapper on top of that file
        """

        self.unit_table = dict()
        self.terrain_grid = []
        self.unit_placements = dict()
        self.player_id_map = dict()
        self.projectiles = dict()
        self.loaded = False
        
        self.target = soldier.Soldier(float(6.0*32),float(7.0*32))
        self.target.image.fill((10,0,0))

        ###Constant Stuff###
        self.tileimage = 'images/tileset.PNG'
        self.width = 800
        self.height = 800
        self.bg = pygame.image.load(self.tileimage).convert()
        self.movement_table = Movement_Table()
        self.movement_table.load('static.txt')
        
        self.colorMap = {0:(0,0,255), 1:(255,0,0), 2:(250,10,0)}
        ###Constant Stuff###

    def update(self, deltaSeconds):
        for player in self.unit_table:
            for e in self.unit_table[player]:
                newbull = e.update(deltaSeconds)
                if newbull is not None:
                    if(self.projectiles.get(player) == None):
                        self.projectiles[player] = []
                    self.projectiles[player].append(newbull)
                e.keep_on_screen(self.width,self.height)
                e.fire_at(self.target)
            
            if(self.projectiles.get(player) == None):
                self.projectiles[player] = []
            for bullet in self.projectiles[player]:
                bullet.update(deltaSeconds)
                
        self.target.update(deltaSeconds)

    def draw(self, screen):
        for i in range(25):
            for j in range(25):
                screen.blit(self.bg,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrain_grid[i])[j])*32,0,32,32))
                
        for player in self.unit_table:
            for unit in self.unit_table[player]:
                unit.draw(screen)
            for bullet in self.projectiles[player]:
                bullet.draw(screen)
                
        if(self.selection != []):
            for unit in self.selection:
                unit.drawfocus(screen)
                
        self.target.draw(screen)
                
    def lookup(self,char):
        return int((self.movement_table.table[char])[0])

    def close(self):
        unit_table = dict()
        terrain_grid = []
        unit_placements = dict()
        self.player_id_map = dict()

    def is_loaded(self):
        return self.loaded

    def load(self,filename):
        if(self.is_loaded() == True):
            self.close()           
                
        self.loaded = True
        ####This is for running the Map####
        self.mouseisdown = False
        self.mouserect = pygame.Rect(0,0,0,0)
        self.selection = []
        ####This is for running the Map####
        
        ###Stuff from Wrapper###
        self.wrapper = Mission_Wrapper.Wrapper()
        self.wrapper.load(filename)
        terrain_list = self.wrapper.GetMap()
        player_list = self.wrapper.GetPlayer()
        unit_list = self.wrapper.GetUnits()
        ###Stuff from Wrapper###
        
        holder = []
        for line in terrain_list:
            for char in line:
                #don't add the trailing newline
                if(char == '\n'):
                    continue
                #append the char to the end of the list 'holder'
                holder[len(holder):] = [char]
            #all chars in 'line' are in holder
            self.terrain_grid.append(holder)
            #set holder to empty
            holder = []
        ###END terrain_grid initialization####

        index = 0
        for player in player_list:
            player.replace('\n','')
            ai_a = ""
            str_type = ''
            res1 = 1
            res2 = 3
            ai_a,str_type,res1,res2 = player.split()
            self.player_id_map[index] = Player()
            self.player_id_map[index].ai = ai_a
            self.player_id_map[index].type = str_type
            self.player_id_map[index].resource = (res1,res2)
            index = index + 1
        ###END player_id_map initialization####
        
        for units in unit_list:
            units.replace('\n','')
            playerobj = self.player_id_map[0]
            #print self.player_id_map
            #print playerobj
            #read each individual unit's line
            x_a = 1
            y_a = 1
            unit_id = 1
            player_id = 0
            x_a,y_a,unit_id,player_id = units.split()
            x_a = float(x_a)
            y_a = float(y_a)
            unit_id = int(unit_id)
            player_id = int(player_id)
            if(int(unit_id) == 3):
                #print "unit was given"
                #print x_a
                #print y_a
                #raw_input('')
                unitobj = building.Building(x_a*32,y_a*32)
                #unitobj.height = 64.0
                #unitobj.width = 64.0
                #unitobj.image = pygame.Surface((unitobj.width, unitobj.height), pygame.SRCALPHA, 32).convert_alpha()
                #unitobj.focus = pygame.Surface((unitobj.width, unitobj.height), pygame.SRCALPHA, 32).convert_alpha()
                #unitobj.rect = pygame.Rect(float(x_a),float(y_a),unitobj.width,unitobj.height)
                #pygame.draw.circle(unitobj.image, (255,0,0), (unitobj.width / 2, unitobj.height / 2), unitobj.width /2)
                #pygame.draw.circle(unitobj.focus, (0,255,0), (unitobj.width / 2, unitobj.height / 2), unitobj.width /2 + 5, 3)
                #unitobj.rect.center = (unitobj.pos.get()[0],unitobj.pos.get()[1])
            else:
                unitobj = soldier.Soldier(x_a*32, y_a*32, self.colorMap[player_id])
            playerobj = self.player_id_map[player_id]
            if(self.unit_table.get(playerobj) == None):
                self.unit_table[playerobj] = []
            self.unit_table[playerobj].append(unitobj)
            self.unit_placements[unitobj] = (x_a,y_a)
            
    def terraincollision(self,unit):
        """
Tests a Unit's rect against the terrain
        """
        Map_Class.Map.get().collision(self)
        too = ((self.terrain_grid[unit.rect.x/32])[unit.rect.y/32])
        if((self.movement_table.table[too])[1]):
            return True
        return False

    def unitcollision(self,unit):
        """
Tests a Unit's rect against all other units' rects
        """
        for player in self.unit_table:
            for unita in self.unit_table[player]:
                if(unita.rect.colliderect(unit.rect)):
                    return True
        return False

    def collision(self,unit):
        """
Composite of unitcollision and terraincollision
        """
        if(self.terraincollision(unit)):
            return True
        if(self.unitcollision(unit)):
            return True
        return False

    # Populates the selection, based on what collides with the given
    # rect
    def select_group(self,rect):
        self.selection = []
        
        player = self.player_id_map[0]
        for unita in self.unit_table[player]:
            if(unita.rect.colliderect(rect)):
                self.selection.append(unita)
    
class Player:
    ai = ""
    type = ""
    resource = (0,0)
    def __init__(self):
        type = ''
