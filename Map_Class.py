import re,Mission_Wrapper,unit,pygame,random,soldier

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
        self.loaded = False
        ###Constant Stuff###
        self.tileimage = 'images/tileset.PNG'
        self.width = 800
        self.height = 800
        self.bg = pygame.image.load(self.tileimage).convert()
        self.movement_table = Movement_Table()
        self.movement_table.load('static.txt')
        ###Constant Stuff###

    def draw(self):
        for i in range(25):
            for j in range(25):
                self.screen.blit(self.bg,pygame.Rect(j*32,i*32,self.width,self.height),pygame.Rect(self.lookup((self.terrain_grid[i])[j])*32,0,32,32))
        for player in self.unit_table:
            for unit in self.unit_table[player]:
                unit.draw(self.screen)
        if(self.selection != []):
            for unit in self.selection:
                unit.drawfocus(self.screen)
        if((self.mouserect.width != 0) or (self.mouserect.height != 0)):
            pygame.draw.rect(self.screen,(175,175,175),self.mouserect,2)
                
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
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
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
            player_id = int(player_id)
            #unitobj = Unit(x_a,y_a,unit_id,player_id)
            unitobj = soldier.Soldier(random.randint(0,self.width),random.randint(0,self.height))
            playerobj = self.player_id_map[player_id]
            if(self.unit_table.get(playerobj) == None):
                self.unit_table[playerobj] = []
                self.unit_table[playerobj].append(unitobj)
            else:
                self.unit_table[playerobj].append(unitobj)
            self.unit_placements[unitobj] = (x_a,y_a)
            
    def terraincollision(self,unit):
        """
Tests a Unit's rect against the terrain
        """
        too = ((self.terrain_grid[unit.rect.x])[unit.rect.y])
        if((self.movement_table.table[too])[1]):
            return False
        return True

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

    def getgroup(self,rect):
        """
returns a list of units that are inside a mouse selection
        """
        holder = []
        for player in self.unit_table:
            for unita in self.unit_table[player]:
                if(unita.rect.colliderect(rect)):
                    holder.append(unita)
        return holder

    def mouseselect(self,tuple1,tuple2):
        """
returns a properly formated rectangle from mouse positions
        """
        #posx = 0
        #posy = 0
        #width = 0
        #height = 0
        #x dimension
        if(tuple1[0] < tuple2[0]):
            #closer to the left
            posx = tuple1[0]
            width = tuple2[0] - tuple1[0]
        else:
            posx = tuple2[0]
            width = tuple1[0] - tuple2[0]
        #y dimension
        if(tuple1[1] < tuple2[1]):
            #closer to the top
            posy = tuple1[1]
            height = tuple2[1] - tuple1[1]
        else:
            posy = tuple2[1]
            height = tuple1[1] - tuple2[1]
            
        return pygame.Rect(posx,posy,width,height)

    def update(self):
        self.clock.tick(50)
        delta_seconds = self.clock.get_time()/1000.0
        events = pygame.event.get()
        for evnt in events:
            if(evnt.type == pygame.QUIT):
                pygame.quit()
            if(evnt.type == pygame.KEYDOWN):
                if(evnt.key == pygame.K_ESCAPE):
                    pygame.quit()
            if(evnt.type == pygame.MOUSEBUTTONDOWN):
                if(evnt.button == 1):
                    self.position1 = evnt.pos
                    self.position2 = pygame.mouse.get_pos()
                    self.mouseisdown = True
                    self.mouserect = self.mouseselect(self.position1,self.position2)
            if(evnt.type == pygame.MOUSEBUTTONUP):
                if(evnt.button == 1):
                    self.position2 = evnt.pos
                    self.mouserect = self.mouseselect(self.position1,self.position2)
                    self.selection = self.getgroup(self.mouserect)
                    self.mouserect = pygame.Rect(0,0,0,0)
                    self.mouseisdown = False
            if(self.mouseisdown):
                self.position2 = pygame.mouse.get_pos()
                self.mouserect = self.mouseselect(self.position1,self.position2)
                    
                    
        for player in self.unit_table:
            for e in self.unit_table[player]:
                e.update(delta_seconds)
                e.keep_on_screen(self.width,self.height)

        
    def run(self):
        while(True):
            self.update()
            self.draw()
            pygame.display.flip()
    
class Player:
    ai = ""
    type = ""
    resource = (0,0)
    def __init__(self):
        type = ''
