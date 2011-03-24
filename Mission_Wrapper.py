class Wrapper:
    """
This class wraps a mission file
each heading has getters/setters
can be used to modify the file
    """
    Intro = []
    Objective = []
    Map = []
    Player = []
    Units = []
    mapname = ""
    
    def __init__(object):
        """
empty initialization
        """
        Intro = []
        Objective = []
        Map = []
        Player = []
        Units = []
        mapname = ""    

    def SetName(self,a):
        """
give a new name to the set of mission data
        """
        self.mapname = a

    def GetName(self):
        """
returns the name of the file currently wrapped
        """
        return self.mapname

    def SetIntro(self,a):
        self.Intro = a

    def GetIntro(self):
        """
returns the introduction (includes newlines)
        """
        return self.Intro

    def SetObjective(self,a):
        """
put in a new list of objectives (do not include newlines)
        """
        self.Objective = a

    def GetObjective(self):
        """
returns the list of Objectives
each objective is in stored format
        """
        return self.Objective

    def SetMap(self,a):
        """
change the terrain of a mission
        """
        self.Map = a

    def GetMap(self):
        """
returns the list of terrain types
each char is a terrain type (a single tile)
        """
        return self.Map

    def SetPlayer(self,a):
        """
Add or remove a Player
        """
        self.Player = a

    def GetPlayer(self):
        """
returns the list of Players
each player is in stored format
        """
        return self.Player

    def SetUnits(self,a):
        """
add or remove a unit from a mission
        """
        self.Units = a

    def GetUnits(self):
        """
returns the list of Units
each unit is in stored format
        """
        return self.Units

    def FormatUnit(Unit unit):
        """
Give a single Unit
return in a single string
all necessary info in that string so that it can be saved
        """

        line = unit.loc.x + ' ' + unit.loc.y + ' ' + unit_type(unit) + ' ' + player_id(unit.owner)

        return line

    def save(self):
        """
Dumps the current state of the mission into a file
        """
        filestream = open(self.mapname,'w')

        filestream.write('[INTRO]')
        filestream.write('\n')
        if(self.Intro != []):
            for line in self.Intro:
                filestream.write(line)
                filestream.write('\n')
        filestream.write('[INTRO]')
        filestream.write('\n')

        filestream.write('[OBJECTIVE]')
        filestream.write('\n')
        if(self.Objective != []):
            for line in self.Objective:
                filestream.write(line)
                filestream.write('\n')
        filestream.write('[OBJECTIVE]')
        filestream.write('\n')

        filestream.write('[MAP]')
        filestream.write('\n')
        if(self.Map != []):
            for line in self.Map:
                filestream.write(line)
                filestream.write('\n')
        filestream.write('[MAP]')
        filestream.write('\n')

        filestream.write('[PLAYERS]')
        filestream.write('\n')
        if(self.Player != []):
            for line in self.Player:
                filestream.write(line)
                filestream.write('\n')
        filestream.write('[PLAYERS]')
        filestream.write('\n')

        filestream.write('[UNITS]')
        filestream.write('\n')
        if(self.Units != []):
            for line in self.Units:
                filestream.write(line)
                filestream.write('\n')
        filestream.write('[UNITS]')
        filestream.write('\n')

        filestream.close()

    def load(self , mission_name):
        """
attempts to load a mission
if that mission file doesnt exist
creates a file with that name (completely empty)
call mission.save() to add header/footers to the file
        """
	filestream = open(mission_name,'a')
	filestream.close()
        filestream = open(mission_name,'r')

        intro_flag = False
        objective_flag = False
        map_flag = False
        player_flag = False
        units_flag = False

        Introa = []
        Objectivea = []
        Mapa = []
        Playera = []
        Unitsa = []

    ####Grab all the info and sort it #########
        for line in filestream:
            if(intro_flag):
                #print 'inside intro'
                if(0<=line.find('[INTRO]')):
                    intro_flag = False
                    continue
                else:
                    Introa.append(line)
            elif(objective_flag):
                if(0<=line.find('[OBJECTIVE]')):
                    objective_flag = False
                    continue
                else:
                    Objectivea.append(line)
            elif(map_flag):
                if(0<=line.find('[MAP]')):
                    map_flag = False
                    continue
                else:
                    Mapa.append(line)
            elif(player_flag):
                if(0<=line.find('[PLAYERS]')):
                    player_flag = False
                    continue
                else:
                    Playera.append(line)
            elif(units_flag):
                if(0<=line.find('[UNITS]')):
                    units_flag = False
                    continue
                else:
                    Unitsa.append(line)

            #Look for the start of a header
            if(0<=line.find('[INTRO]')):
                intro_flag = True
                continue
            if(0<=line.find('[OBJECTIVE]')):
                objective_flag = True
                continue
            if(0<=line.find('[MAP]')):
                map_flag = True
                continue
            if(0<=line.find('[PLAYERS]')):
                player_flag = True
                continue
            if(0<=line.find('[UNITS]')):
                units_flag = True
                continue
    ######### END FOR LINE IN FILESTREAM ########

        filestream.close()
        self.mapname = mission_name
        self.Intro = Introa
        self.Objective = Objectivea
        self.Map = Mapa
        self.Player = Playera
        self.Units = Unitsa
    ###END MISSION LOAD###

    
