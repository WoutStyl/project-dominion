import pygame, math, sys, string, os, menu, map, queueitem
#Responsibilities:
#Draws itself
#Responds to Mouse Position

#Collaborators:
#OnClick
#Mouse
#Surface

class Button(object):
    def __init__(self, x,y, text, clickType,targetImage, focused = False):
        self.height = 64
        self.width = 256
        self.pos = [x,y]
        self.nowFocused = focused
        self.name = targetImage
        self.clickObj = clickType
        self.buttonText = text
        self.enabled = True
        
        self.image = self.load_image(targetImage + ".png")
        self.imageFocused = self.load_image(targetImage + "Focused.png")
        self.rect = self.image.get_rect()
        if focused:
            self.focus()
        else:
            self.unfocus()
                
    def update(self):
        pass
        
    def draw(self,screen):
        if not self.enabled:
            return
        if self.nowFocused:
            screen.blit(self.imageFocused, (self.pos[0], self.pos[1]))
        else:
            screen.blit(self.image, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
    def changeImage(self, targetImage):
        #self.image, self.rect = self.load_image(targetImage)
        self.name = targetImage
    def unfocus(self):
        self.nowFocused = False
    def focus(self):
        self.nowFocused = True
    def load_image(self, dispName):
        fullname = os.path.join('images', dispName)
        try:
            image = pygame.transform.scale(pygame.image.load(fullname), (self.width, self.height))
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        return image.convert()
    def is_mouse_focus(self):
        if not self.enabled:
            return False
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.width:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.height:
                self.focus()
                return True
        return False
        
    def is_enabled(self):
        return self.enabled
        
    def clicked(self, m):
        if not self.enabled:
            return
        self.clickObj.clicked(m)
        
    def unclicked(self, m):
        if not self.enabled:
            return
        self.clickObj.unclicked(m)
        
    def force_unclicked(self):
        self.clickObj.force_unclicked()
        
    def set_enabled(self, value):
        self.enabled = value
        
    def is_enabled(self):
        return self.enabled

#Responsibilities
#Defines logic for click events

#Collaborators
#Menu   

class OnClick(object):
    def __init__(self):
        self.isClicked = False
            
    def is_clicked(self):
        return self.isClicked
        
    def clicked(self, m):
        pygame.mouse.get_rel()
        self.isClicked = True
        
    def unclicked(self, m):
        self.isClicked = False
        
    def force_unclicked(self):
        self.isClicked = False

class StartOnClick(OnClick) :
    def unclicked(self, m):
        super(StartOnClick, self).unclicked(m)
        self.menu = m
        m.bInMenu = False

class LoadOnClick(OnClick) :
    def unclicked(self, m):
        super(LoadOnClick, self).unclicked(m)
        self.menu = m
        tempMap = map.Map.get()
        tempMap.load(self.mission)
        m.bInMenu = False
        print map
        print "Mission Loaded"
        
    def setMission(self, mission):
        print "Mission Set:"
        self.mission = mission
        print self.mission

class MissionSelectOnClick(OnClick):
    def unclicked(self,m):
        super(MissionSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.MissionSelectMenu()

class SavedMissionSelectOnClick(OnClick):
    def unclicked(self,m):
        super(SavedMissionSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.SavedMissionSelectMenu()
                
class SavedCampaignSelectOnClick(OnClick):
    def unclicked(self,m):
        super(SavedCampaignSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.SavedCampaignSelectMenu()

class AddToQueueOnClick(OnClick):
    def __init__(self, building = None):
        self.isClicked = False
        self.building = building
    def unclicked(self,m):
        super(AddToQueueOnClick, self).unclicked(m)
        self.building.add_to_queue()

class BackOnClick(OnClick):
    def unclicked(self, m):
        super(BackOnClick, self).unclicked(m)
        m.leave_menu()
        
                
                
	
		
