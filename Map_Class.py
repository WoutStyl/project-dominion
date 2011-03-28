import re
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
        for line in filesteam:
            char_a,id_a,pass_a = line.split()
            table[char_a] = (id_a,pass_a)    

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
    player_id_map = dict()
    movement_table = ""

    def __init__(self, terrain_list, unit_list, player_list):
        """
So when you want to create a new Map object you want to
pass it the terrain_list and unit_list gotten from
Mission_Wrapper ("Map" and "Units" respectively)
        """
        movement_table = Movement_Table()
        movement_table.load('static.txt')
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
            ai_a = True
            str_type = ''
            res1 = 1
            res2 = 3
            ai_a,str_type,res1,res2 = player.split()
            player_id_map[index] = Player()
            player_id_map[index].ai = ai_a
            player_id_map[index].type = str_type
            player_id_map[index].resource = Resource(res1,res2)
            index = index + 1

        for unit in unit_list:
            #read each individual unit's line
            x_a = 1
            y_a = 1
            unit_id = 1
            player_id = 1
            x_a,y_a,unit_id,player_id = unit.split()
            unitobj = Unit(x_a,y_a,unit_id,player_id)
            unit_table[player_id_map[player_id]].append(unitobj)
            unit_placement[unitobj] = Location(x_a,y_a)

    def collision(self,unit,movement):
        too = ((self.terrain_grid[unit.location.x+movement.x])[unit.location.y+movement.y])
        if((self.movement_table.table[too])[1]):
            return False
        return True
    
