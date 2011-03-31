import re,Mission_Wrapper,unit,pygame,random,soldier
class Location:
    """
Simple (x,y) format
    """
    x = 0
    y = 0
    def __init__(self,a,b):
        self.x = a
        self.y = b

class Movement_Table:
    """
This class associates a terrain type with its properties
    """
    table = dict()
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
    unit_table = dict()
    terrain_grid = []
    unit_placements = dict()
    tileimage = 'tileset.PNG'
    width = 800
    height = 800

    def __init__(self, filename):
        """
So when you want to create a new Map object you want to
pass it the terrain_list and unit_list gotten from
Mission_Wrapper ("Map" and "Units" respectively)
        """
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load(self.tileimage).convert()
        self.wrapper = Mission_Wrapper.Wrapper()
        self.wrapper.load(filename)
        self.player_id_map = dict()
        terrain_list = self.wrapper.Map
        player_list = self.wrapper.Player
        unit_list = self.wrapper.Units
        self.movement_table = Movement_Table()
        self.movement_table.load('static.txt')
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
            #unitobj = unit.Unit(x_a,y_a)
            playerobj = self.player_id_map[player_id]
            #print player_id
            #print self.player_id_map
            """if(player_id == '0'):
                playerobj = self.player_id_map[0]
            elif(player_id == '1'):
                playerobj = self.player_id_map[1]
            elif(player_id == '2'):
                playerobj = self.player_id_map[2]
            else:
                playerobj = self.player_id_map.get(3)"""
            #print playerobj
            if(self.unit_table.get(playerobj) == None):
                self.unit_table[playerobj] = []
                self.unit_table[playerobj].append(unitobj)
            else:
                self.unit_table[playerobj].append(unitobj)
            self.unit_placements[unitobj] = (x_a,y_a)
            #print self.unit_table

    def draw(self):
        for i in range(25):
            for j in range(25):
                self.screen.blit(self.bg,pygame.Rect(i*32,j*32,self.width,self.height),pygame.Rect(self.lookup((self.terrain_grid[i])[j])*32,0,32,32))
        for player in self.unit_table:
            for unit in self.unit_table[player]:
                unit.draw(self.screen)
                
                
    def lookup(self,char):
        return int((self.movement_table.table[char])[0])

    def collision(self,unit,movement):
        too = ((self.terrain_grid[unit.location.x+movement.x])[unit.location.y+movement.y])
        if((self.movement_table.table[too])[1]):
            return False
        return True

    def update(self):
        self.clock.tick(50)
        delta_seconds = self.clock.get_time()/1000.0
        events = pygame.event.get()
        for evnt in events:
            if(evnt.type == pygame.KEYDOWN):
                if(evnt.key == pygame.K_ESCAPE):
                    pygame.quit()
                    
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
