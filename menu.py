import pygame, math, sys, string, os, missionwrapper, button

class Menu(object):
    def __init__(self, screen):
        self.buttons = []
        self.screen = screen
        self.index = 0
        self.bInMenu = True
        self.mission = ""
        self.nextMenu = self
            
            
    def add_button(self, x,y,text,clicktype, targetImage = "Blank"):
        # print len(self.buttons)
        if len(self.buttons) == 0:
            theButton = button.Button(x,y,text,clicktype,targetImage,True)
                
        else:
            theButton = button.Button(x,y,text,clicktype,targetImage,False)
        self.buttons.append(theButton)
    def draw(self,screen):
        for b in self.buttons:
            b.draw(screen)
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print "Keypress Down: "
                self.buttons[self.index].nowFocused = False
                self.index -= 1
                if self.index < 0:
                        self.index = len(self.buttons)-1
                print self.index
                self.buttons[self.index].nowFocused = True
            if event.key == pygame.K_DOWN:
                print "Keypress Up: "
                self.buttons[self.index].nowFocused = False
                self.index += 1
                if self.index >= len(self.buttons):
                        self.index = 0
                print self.index
                self.buttons[self.index].nowFocused = True
            if event.key == pygame.K_RETURN:
                print "Return!"
                self.buttons[self.index].clickObj.isClicked(self)
            if event.key == pygame.K_ESCAPE:
                self.leave_menu()
        if event.type == pygame.USEREVENT+1:
            print "YAY!"
            self.bInMenu = False
        if event.type == pygame.QUIT:
            sys.exit(0)
    def update(self):
        if(self.bInMenu):
            for event in pygame.event.get():
                self.handle_event(event)
        return self.nextMenu
    def leave_menu(self):
        self.bInMenu = False

class MainMenu(Menu):
    def __init__(self,screen):
        super(MainMenu, self).__init__(screen)
        buttonlocx = 300
        buttonlocx -= 128
        buttonlocy = 300
        buttonlocy -= 96
        font = pygame.font.Font(None, 36)
        text = font.render("", 1, (0,0,0))
        self.add_button(buttonlocx, (buttonlocy -128), text, button.StartOnClick(), "StartCampaign")
        self.add_button(buttonlocx,buttonlocy,text, button.MissionSelectOnClick(), "StartMission")
        self.add_button(buttonlocx,(buttonlocy+128),text, button.SavedCampaignSelectOnClick(), "LoadCampaign")
        self.add_button(buttonlocx,(buttonlocy+256),text, button.SavedMissionSelectOnClick(), "LoadMission")
    
class MissionSelectMenu(Menu):
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
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "mission%d.txt" % (i,)
            pathstring = os.path.join("missions", filename)
    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen)

class SavedMissionSelectMenu(Menu):
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
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedMission%d.txt" % (i,)
            pathstring = os.path.join("savedMissions", filename)
    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen)

class SavedCampaignSelectMenu(Menu):
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
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedCampaign%d.txt" % (i,)
            pathstring = os.path.join("savedCampaigns", filename)

    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen)
        

            

            

