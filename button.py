import pygame, math, sys, string, os, menu, map, queueitem

class Button(object):
    def __init__(self, x,y, text, clickType,targetImage, focused = False):
        self.height = 64
        self.width = 256
        self.pos = [x,y]
        self.nowFocused = focused
        self.name = targetImage
        self.clickObj = clickType
        self.buttonText = text
        if focused:
            self.focus()
        else:
            self.unfocus()
                
    def draw(self,screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
    def changeImage(self, targetImage):
        #self.image, self.rect = self.load_image(targetImage)
        self.name = targetImage        
    def unfocus(self):
        dispName = self.name + ".png"
        self.load_image(dispName)
    def focus(self):
        dispName = self.name + "Focused.png"
        self.load_image(dispName)
    def load_image(self, dispName):
        fullname = os.path.join('images', dispName)
        try:
            image = pygame.transform.scale(pygame.image.load(fullname), (self.width, self.height))
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        self.image = image.convert()
        self.rect = image.get_rect()
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
    def set_queue(self, unitQueue):
        self.queue = unitQueue
                
                
	
		
