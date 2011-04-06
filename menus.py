import pygame, math, sys, string, os, Mission_Wrapper, button, menu

class MainMenu(menu.Menu):
    def __init__(self,screen):
        super(MainMenu, self).__init__(screen)
        buttonlocx = 300
        buttonlocx -= 128
        buttonlocy = 300
        buttonlocy -= 96
        font = pygame.font.Font(None, 36)
        text = font.render("", 1, (0,0,0))
        self.addButton(buttonlocx, (buttonlocy -128), text, button.StartOnClick(), "StartCampaign")
        self.addButton(buttonlocx,buttonlocy,text, button.MissionSelectOnClick(), "StartMission")
        self.addButton(buttonlocx,(buttonlocy+128),text, button.SavedCampaignSelectOnClick(), "LoadCampaign")
        self.addButton(buttonlocx,(buttonlocy+256),text, button.SavedMissionSelectOnClick(), "LoadMission")
    
class MissionSelectMenu(menu.Menu):
    def __init__(self,screen):
        i = 0
        super(MissionSelectMenu, self).__init__(screen)
        filename = "mission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("missions", filename)
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.addButton(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "mission%d.txt" % (i,)
            pathstring = os.path.join("missions", filename)
    def leaveMenu(self):
        self.nextMenu = MainMenu(self.screen)

class SavedMissionSelectMenu(menu.Menu):
    def __init__(self,screen):
        i = 0
        super(SavedMissionSelectMenu, self).__init__(screen)
        filename = "savedMission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedMissions", filename)
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.addButton(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedMission%d.txt" % (i,)
            pathstring = os.path.join("savedMissions", filename)
    def leaveMenu(self):
        self.nextMenu = MainMenu(self.screen)

class SavedCampaignSelectMenu(menu.Menu):
    def __init__(self,screen):
        i = 0
        super(SavedCampaignSelectMenu, self).__init__(screen)
        filename = "savedCampaign%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedCampaigns", filename)
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.addButton(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedCampaign%d.txt" % (i,)
            pathstring = os.path.join("savedCampaigns", filename)

    def leaveMenu(self):
        self.nextMenu = MainMenu(self.screen)
        
