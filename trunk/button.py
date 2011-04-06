import pygame, math, sys, string, os, menu, Map_Class, queueitem

class Button(object):
    def __init__(self, x,y, text, clickType,targetImage, focused = False):
        self.height = 64
        self.width = 256
        self.pos = [x,y]
        self.nowFocused = focused
        self.name = targetImage
        self.image, self.rect = self.load_image()
        self.clickObj = clickType
        self.buttonText = text
                
    def draw(self,screen):
        self.image, self.rect = self.load_image()
        screen.blit(self.image, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
    def changeImage(self, targetImage):
        #self.image, self.rect = self.load_image(targetImage)
        self.name = targetImage
    def load_image(self, colorkey = None):
        if self.nowFocused is True:
            dispName = self.name + "Focused.png"
        else:
            dispName = self.name +".png"
        fullname = os.path.join('images', dispName)
        try:
            image = pygame.transform.scale(pygame.image.load(fullname),(self.width, self.height))
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
		
class OnClick(object):
    def __init__(self):
        self.clicked = False
            
    def isClicked(self, m):
        self.clicked = True
    def unclicked(self):
        self.clicked = False

class StartOnClick(OnClick) :
    def isClicked(self, m):
        self.clicked = True
        self.menu = m
        m.bInMenu = False

class LoadOnClick(OnClick) :
    def isClicked(self, m):
        self.clicked = True
        self.menu = m
        map = Map_Class.Map.get()
        map.load(self.mission)
        m.bInMenu = False
        print map
        print "Mission Loaded"
    def setMission(self, mission):
        print "Mission Set:"
        self.mission = mission
        print self.mission

class MissionSelectOnClick(OnClick):
    def isClicked(self,m):
        m.nextMenu = menu.MissionSelectMenu(m.screen)
    def draw(self):
        self.menu.screen.fill((0,0,0))
        fullname = os.path.join('images', 'MissionSelect.png')
        image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
        self.menu.screen.blit(image, (172, 20 ))
            
    def update(self):
        self.draw()

class SavedMissionSelectOnClick(OnClick):
    def isClicked(self,m):
        m.nextMenu = menu.SavedMissionSelectMenu(m.screen)

    def draw(self):
        self.menu.screen.fill((0,0,0))
        fullname = os.path.join('images', 'SavedMissionSelect.png')
        image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
        self.menu.screen.blit(image, (172, 20 ))
            
    def update(self):
        self.draw()
                
class SavedCampaignSelectOnClick(OnClick):
    def isClicked(self,m):
        m.nextMenu = menu.SavedCampaignSelectMenu(m.screen)

    def draw(self):
        self.menu.screen.fill((0,0,0))
        fullname = os.path.join('images', 'savedCampaignSelect.png')
        image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
        self.menu.screen.blit(image, (172, 20 ))
            
    def update(self):
        self.draw()

class AddToQueueOnClick(OnClick):
    def __init__(self):
        self.clicked = False
        self.queue = []
    def isClicked(self,m):
        self.queue.append(queueitem.QueueItem(self.queue))
        print "Yay!"
                
                
                
	
		
