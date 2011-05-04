import pygame, math, sys, string, os, missionwrapper, map

# This class manages menus and their proeprties
class Menu(object):
    def __init__(self):
        self.buttons = []
        self.index = 0
        self.bInMenu = True
        self.mission = ""
        self.nextMenu = self
        self.stealInput = False
        self.clickedButton = None
        self.lastFocused = False
            
    # add_button
    # This function adds a button to the menu given x and y coordinates,
    # text, desired click functionality and image
    def add_button(self, x,y,text,clicktype, targetImage = "Blank", enabled = True, height = 64, width = 256):
        # If this is the first button, set it to be focused by default
        if len(self.buttons) == 0:
            theButton = button.Button(x,y,text,clicktype,targetImage,True, enabled, height, width)
                
        else:
            theButton = button.Button(x,y,text,clicktype,targetImage,False, enabled, height, width)
        self.buttons.append(theButton)
    def draw(self,screen):
        for b in self.buttons:
            b.draw(screen)
    # handle_event
    # Handles user input in the menu system
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.stealInput is True:
                self.buttons[self.index].unfocus()
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.buttons)-1
                self.buttons[self.index].focus()
                return True
            if event.key == pygame.K_DOWN and self.stealInput is True:
                self.buttons[self.index].unfocus()
                self.index += 1
                if self.index >= len(self.buttons):
                    self.index = 0
                self.buttons[self.index].focus()
                return True
            if event.key == pygame.K_RETURN:
                self.buttons[self.index].unclicked(self)
                return True
            if event.key == pygame.K_ESCAPE:
                self.leave_menu()
                return True
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.buttons[self.index].is_mouse_focus():
                    self.buttons[self.index].clicked(self)
                    self.buttons[self.index].focus()
                    self.clickedButton = self.buttons[self.index]
                    return True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.clickedButton != None:
                    self.clickedButton.force_unclicked()
                    self.clickedButton = None
                if self.buttons[self.index].is_mouse_focus():
                    self.buttons[self.index].unclicked(self)
                    self.buttons[self.index].focus()
                    return True
        return False
    # update
    # Calls the event handler
    def update(self):
        #if(self.bInMenu):
            #for event in pygame.event.get():
                #self.handle_event(event)
        return self.nextMenu
    # leave_menu
    # Causes the game loop to exit the main menu when the escape key is hit
    def leave_menu(self):
        self.bInMenu = False
    def check_focus(self):
        newIndex = len(self.buttons)-1
        for bttn in reversed(self.buttons):
            if bttn.is_mouse_focus() is True:
                self.buttons[newIndex].focus()
                if self.index is not newIndex and self.index < len(self.buttons):
                    self.buttons[self.index].unfocus()
                self.index = newIndex
                self.lastFocused = True
                return
            else:
                newIndex -= 1
                
        if self.lastFocused:
            if self.index < len(self.buttons):
                self.buttons[self.index].unfocus()
                self.index = len(self.buttons)-1
                self.lastMousePos = pygame.mouse.get_pos()
                self.lastFocused = False

        
#These classes initialize the menu differently based on its intended purpose

class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__()
        buttonlocx = 300
        buttonlocx -= 128
        buttonlocy = 300
        buttonlocy -= 96
        font1 = pygame.font.Font(None, 36)
        text = font1.render("", 1, (0,0,0))
        self.stealInput = True
        #Buttons for sub menus
        self.add_button(buttonlocx, (buttonlocy -128), text, button.StartOnClick(), "StartCampaign",False)
        self.add_button(buttonlocx,buttonlocy,text, button.MissionSelectOnClick(), "StartMission")
        self.add_button(buttonlocx,(buttonlocy+128),text, button.SavedCampaignSelectOnClick(), "LoadCampaign")
        self.add_button(buttonlocx,(buttonlocy+256),text, button.SavedMissionSelectOnClick(), "LoadMission")
    def draw(self, screen):
        screen.fill((0,0,0))
        super(MainMenu,self).draw(screen)
        
        
# Sub-Menus
# These menus also modify the leave_menu function, which is used in sub-menus to 
# return the user to the Main Menu when the escape key is pressed
        
class MissionSelectMenu(Menu):
    def __init__(self):
        i = 0
        super(MissionSelectMenu, self).__init__()
        filename = "mission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("missions", filename)
        self.stealInput = True
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
        self.nextMenu = MainMenu() # The next menu loaded will be the Main Menu
    def draw(self, screen):
        screen.fill((0,0,0))
        super(MissionSelectMenu,self).draw(screen)

class SavedMissionSelectMenu(Menu):
    def __init__(self):
        i = 0
        super(SavedMissionSelectMenu, self).__init__()
        filename = "savedMission%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedMissions", filename)
        self.stealInput = True
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
        self.nextMenu = MainMenu() # The next menu loaded will be the Main Menu
    def draw(self, screen):
        screen.fill((0,0,0))
        super(SavedMissionSelectMenu,self).draw(screen)

class SavedCampaignSelectMenu(Menu):
    def __init__(self):
        i = 0
        super(SavedCampaignSelectMenu, self).__init__()
        filename = "savedCampaign%d.txt" % (i,)
        initx = 300 - 128
        inity = 300-128
        pathstring = os.path.join("savedCampaigns", filename)
        self.stealInput = True
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
        self.nextMenu = MainMenu() # The next menu loaded will be the Main Menu
    def draw(self, screen):
        screen.fill((0,0,0))
        super(SavedCampaignSelectMenu,self).draw(screen)

class UnitMenu(Menu):
    def __init__(self):
        super(UnitMenu, self).__init__()
        font = pygame.font.Font(None, 36)
        text = font.render("Protocol",1,(0,0,0))
        Click = button.ProtocolDisplayToggleOnClick()
        self.add_button(572,536,text,Click, "Blank", True, 64, 128)
        self.protocolButtons = []
        self.modifierButtons = []
        self.menuButtons = self.buttons
        self.showProtocols = False
        self.currentProtocol = 0
        self.nextMenu = self
        print "Init"

    def update(self):
        font = pygame.font.Font(None, 36)
        i = 1
        theMap = map.Map.get()
        probuttons = []
        while len(theMap.protocols) > len(probuttons):
            name = str(i)
            text = font.render(name,1,(0,0,0))
            Click = button.SelectProtocolOnClick(i)
            height = (i-1) * 70
            newButton = button.Button(600, height, text, Click, "Blank",False, True, 64, 64)
            probuttons.append(newButton)
            i+=1
        self.protocolButtons = probuttons
        modbuttons = []
        listlength = len(self.protocolButtons)
        Click = button.NewProtocolOnClick()
        name = "New"
        text = font.render(name,1,(0,0,0))
        height = listlength * 70
        newButton = button.Button(600,height,text,Click,"Blank",False,True,64,64)
        modbuttons.append(newButton)
        listlength +=1
        # Click = button.EditProtocolOnClick()
        # name = "Edit"
        # text = font.render(name,1,(0,0,0))
        # height = listlength * 70
        # newButton = button.Button(600,height,text,Click,"Blank",False,True,64,64)
        # modbuttons.append(newButton)
        # listlength +=1
        Click = button.SetProtocolOnClick()
        name = "Set"
        text = font.render(name,1,(0,0,0))
        height = listlength * 70
        newButton = button.Button(600,height,text,Click,"Blank",False,True,64,64)
        modbuttons.append(newButton)
        listlength +=1
        Click = button.DeleteProtocolOnClick()
        name = "Delete"
        text = font.render(name,1,(0,0,0))
        height = listlength * 70
        newButton = button.Button(600,height,text,Click,"Blank",False,True,64,64)
        modbuttons.append(newButton)
        
        self.modifierButtons = modbuttons

        if self.showProtocols is True:
            self.buttons = self.menuButtons + self.protocolButtons + self.modifierButtons
        else:
            self.buttons = self.menuButtons
            
        for b in self.buttons:
            b.set_visible(True)
            b.set_enabled(True)
            b.update()
        #self.buttons = self.menuButtons
        return self.nextMenu
    def draw(self,screen):
        for b in self.buttons:
            b.draw(screen)
    def set_protocols_visible(self, value):
        self.showProtocols = value

class BuildMenu(UnitMenu):
    def __init__(self, building):
        super(BuildMenu, self).__init__()
        font = pygame.font.Font(None, 36)
        text = font.render("Add",1,(0,0,0))
        Click = button.AddToQueueOnClick(building)
        self.add_button(500, 536, text, Click, "Blank", True, 64, 64)


import button
        
        
        

            

            

