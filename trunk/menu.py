import pygame, math, sys, string, os, missionwrapper, button

# This class manages menus and their proeprties
class Menu(object):
    def __init__(self, screen):
        self.buttons = []
        self.screen = screen
        self.index = 0
        self.bInMenu = True
        self.mission = ""
        self.nextMenu = self
            
    # add_button
    # This function adds a button to the menu given x and y coordinates,
    # text, desired click functionality and image
    def add_button(self, x,y,text,clicktype, targetImage = "Blank"):
        # If this is the first button, set it to be focused by default
        if len(self.buttons) == 0:
            theButton = button.Button(x,y,text,clicktype,targetImage,True)
                
        else:
            theButton = button.Button(x,y,text,clicktype,targetImage,False)
        self.buttons.append(theButton)
    def draw(self,screen):
        for b in self.buttons:
            b.draw(screen)
    # handle_event
    # Handles user input in the menu system
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print "Keypress Down: "
                self.buttons[self.index].unfocus()
                self.index -= 1
                if self.index < 0:
                        self.index = len(self.buttons)-1
                print self.index
                self.buttons[self.index].focus()
            if event.key == pygame.K_DOWN:
                print "Keypress Up: "
                self.buttons[self.index].unfocus()
                self.index += 1
                if self.index >= len(self.buttons):
                        self.index = 0
                print self.index
                self.buttons[self.index].focus()
            if event.key == pygame.K_RETURN:
                print "Return!"
                self.buttons[self.index].clickObj.isClicked(self)
            if event.key == pygame.K_ESCAPE:
                self.leave_menu()
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clickFocus()
    # update
    # Calls the event handler
    def update(self):
        if(self.bInMenu):
            for event in pygame.event.get():
                self.handle_event(event)
        return self.nextMenu
    # leave_menu
    # Causes the game loop to exit the main menu when the escape key is hit
    def leave_menu(self):
        self.bInMenu = False
    def check_focus(self):
        newIndex = 0
        for bttn in self.buttons:
            if bttn.is_mouse_focus() is True:
                self.buttons[newIndex].focus()
                if self.index is not newIndex:
                    self.buttons[self.index].unfocus()
                self.index = newIndex
                return
            else:
                newIndex += 1
    def clickFocus(self):
        self.buttons[self.index].clickObj.isClicked(self)
        self.buttons[self.index].focus()

        
#These classes initialize the menu differently based on its intended purpose

class MainMenu(Menu):
    def __init__(self,screen):
        super(MainMenu, self).__init__(screen)
        buttonlocx = 300
        buttonlocx -= 128
        buttonlocy = 300
        buttonlocy -= 96
        font = pygame.font.Font(None, 36)
        text = font.render("", 1, (0,0,0))
        #Buttons for sub menus
        self.add_button(buttonlocx, (buttonlocy -128), text, button.StartOnClick(), "StartCampaign")
        self.add_button(buttonlocx,buttonlocy,text, button.MissionSelectOnClick(), "StartMission")
        self.add_button(buttonlocx,(buttonlocy+128),text, button.SavedCampaignSelectOnClick(), "LoadCampaign")
        self.add_button(buttonlocx,(buttonlocy+256),text, button.SavedMissionSelectOnClick(), "LoadMission")

# Sub-Menus
# These menus also modify the leave_menu function, which is used in sub-menus to 
# return the user to the Main Menu when the escape key is pressed
        
class MissionSelectMenu(Menu):
    def __init__(self,screen):
        i = 0
        super(MissionSelectMenu, self).__init__(screen)
        filename = "mission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("missions", filename)
        # Look in the "missions" folder for files of the form "mission#.txt"
        # and add a new button to the menu for each mission file.
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "mission%d.txt" % (i,)
            pathstring = os.path.join("missions", filename)
        text = font.render("Back", 1, (10,10,10))
        self.add_button(525, (525), text, button.BackOnClick(), "Blank")
    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen) # The next menu loaded will be the Main Menu

class SavedMissionSelectMenu(Menu):
    def __init__(self,screen):
        i = 0
        super(SavedMissionSelectMenu, self).__init__(screen)
        filename = "savedMission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedMissions", filename)
        # Look in the "savedMissions" folder for files of the form "savedMission#.txt"
        # and add a new button to the menu for each savedMission file.
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedMission%d.txt" % (i,)
            pathstring = os.path.join("savedMissions", filename)
        text = font.render("Back", 1, (10,10,10))
        self.add_button(525, (525), text, button.BackOnClick(), "Blank")
    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen) # The next menu loaded will be the Main Menu

class SavedCampaignSelectMenu(Menu):
    def __init__(self,screen):
        i = 0
        super(SavedCampaignSelectMenu, self).__init__(screen)
        filename = "savedCampaign%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedCampaigns", filename)
        # Look in the "savedCampaigns" folder for files of the form "savedCampaign#.txt"
        # and add a new button to the menu for each savedCampaign file.
        while(os.path.isfile(pathstring)):
            LC = button.LoadOnClick()
            LC.setMission(pathstring)
            font = pygame.font.Font(None, 36)
            text = font.render(filename, 1, (10,10,10))
            self.add_button(initx, inity +(64*i), text, LC, "Blank")
            i += 1
            filename = "savedCampaign%d.txt" % (i,)
            pathstring = os.path.join("savedCampaigns", filename)
        text = font.render("Back", 1, (10,10,10))
        self.add_button(525, (525), text, button.BackOnClick(), "Blank")

    def leave_menu(self):
        self.nextMenu = MainMenu(self.screen) # The next menu loaded will be the Main Menu
        

            

            
