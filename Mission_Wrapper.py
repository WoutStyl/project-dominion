class Wrapper:
    Intro = []
    Objective = []
    Map = []
    Player = []
    Units = []
    mapname = ""
    
    def __init__(object):
        pass

    def SetName(a):
        mapname = a

    def GetName():
        return mapname

    def SetIntro(a):
        Intro = a

    def GetIntro():
        return Intro

    def SetObjective(a):
        Objective = a

    def GetObjective():
        return Objective

    def SetMap(a):
        Map = a

    def GetMap():
        return Map

    def SetPlayer(a):
        Player = a

    def GetPlayer():
        return Player

    def SetUnits(a):
        Units = a

    def GetUnits():
        return Units

    def save():
        filestream = open(mapname)

        filestream.write('[INTRO]')
        filestream.write('\n')
        for line in Intro:
            filestream.write(line)
            filestream.write('\n')
        filestream.write('[INTRO]')
        filestream.write('\n')

        filestream.write('[OBJECTIVE')
        filestream.write('\n')
        for line in Objective:
            filestream.write(line)
            filestream.write('\n')
        filestream.write('[OBJECTIVE]')
        filestream.write('\n')

        filestream.write('[MAP]')
        filestream.write('\n')
        for line in Map:
            filestream.write(line)
            filestream.write('\n')
        filestream.write('[MAP]')
        filestream.write('\n')

        filestream.write('[PLAYERS]')
        filestream.write('\n')
        for line in Player:
            filestream.write(line)
            filestream.write('\n')
        filestream.write('[PLAYERS]')
        filestream.write('\n')

        filestream.write('[UNITS]')
        filestream.write('\n')
        for line in Units:
            filestream.write(line)
            filestream.write('\n')
        filestream.write('[UNITS]')
        filestream.write('\n')

        filestream.close()

    def load_mission(myclass , mission_name):
        filestream = open(mission_name)

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
        myclass.mapname = mission_name
        myclass.Intro = Introa
        myclass.Objective = Objectivea
        myclass.Map = Mapa
        myclass.Player = Playera
        myclass.Units = Unitsa
    ###END MISSION LOAD###

    
