import pygame, math, sys, string, os, Mission_Wrapper

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
                missionfile = Mission_Wrapper.Wrapper()
                missionfile.load(self.mission)
                print "Mission Loaded"
        def setMission(self, mission):
                print "Mission Set:"
                self.mission = mission
                print self.mission

class MissionSelectOnClick(OnClick):
        def isClicked(self,m):
                self.menu = m
                SelectMenu = Menu(m.screen)
                SelectMenu.bInMenu = True
                i = 0
                filename = "mission%d.txt" % (i,)
                initx = 300 - 128
                inity = 300-128
                pathstring = os.path.join("missions", filename)
                while(os.path.isfile(pathstring)):
                        print filename
                        LC = LoadOnClick()
                        print pathstring
                        LC.setMission(pathstring)
                        font = pygame.font.Font(None, 36)
                        text = font.render(filename, 1, (10,10,10))
                        SelectMenu.addButton(initx, inity +(64*i), text, LC, "Blank")
                        i += 1
                        filename = "mission%d.txt" % (i,)
                        pathstring = os.path.join("missions", filename)
                while SelectMenu.bInMenu:
                        self.update()
                        SelectMenu.update()
                        SelectMenu.draw(m.screen)
                        pygame.display.flip()
        def draw(self):
                self.menu.screen.fill((0,0,0))
                fullname = os.path.join('images', 'MissionSelect.png')
                image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
                self.menu.screen.blit(image, (172, 20 ))
                
        def update(self):
                self.draw()

class SavedMissionSelectOnClick(OnClick):
        def isClicked(self,m):
                self.menu = m
                SelectMenu = Menu(m.screen)
                i = 0
                filename = "savedMission%d.txt" % (i,)
                initx = 300 - 128
                inity = 300-128
                pathstring = os.path.join("savedMissions", filename)
                while(os.path.isfile(pathstring)):
                        print filename
                        LC = LoadOnClick()
                        print pathstring
                        LC.setMission(pathstring)
                        font = pygame.font.Font(None, 36)
                        text = font.render(filename, 1, (10,10,10))
                        SelectMenu.addButton(initx, inity +(64*i), text, LC, "Blank")
                        i += 1
                        filename = "savedMission%d.txt" % (i,)
                        pathstring = os.path.join("savedMissions", filename)
                while SelectMenu.bInMenu:
                        self.update()
                        SelectMenu.update()
                        SelectMenu.draw(m.screen)
                        pygame.display.flip()
        def draw(self):
                self.menu.screen.fill((0,0,0))
                fullname = os.path.join('images', 'SavedMissionSelect.png')
                image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
                self.menu.screen.blit(image, (172, 20 ))
                
        def update(self):
                self.draw()
                
class SavedCampaignSelectOnClick(OnClick):
        def isClicked(self,m):
                self.menu = m
                m.bInMissionSelect = True
                SelectMenu = Menu(m.screen)
                SelectMenu.bInMenu = True
                i = 0
                filename = "savedCampaign%d.txt" % (i,)
                initx = 300 - 128
                inity = 300-128
                pathstring = os.path.join("savedCampaigns", filename)
                while(os.path.isfile(pathstring)):
                        print filename
                        LC = LoadOnClick()
                        print pathstring
                        LC.setMission(pathstring)
                        font = pygame.font.Font(None, 36)
                        text = font.render(filename, 1, (10,10,10))
                        SelectMenu.addButton(initx, inity +(64*i), text, LC, "Blank")
                        i += 1
                        filename = "savedCampaign%d.txt" % (i,)
                        pathstring = os.path.join("savedCampaigns", filename)
                while SelectMenu.bInMenu:
                        self.update()
                        SelectMenu.update()
                        SelectMenu.draw(m.screen)
                        pygame.display.flip()
        def draw(self):
                self.menu.screen.fill((0,0,0))
                fullname = os.path.join('images', 'savedCampaignSelect.png')
                image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
                self.menu.screen.blit(image, (172, 20 ))
                
        def update(self):
                self.draw()
                
                
                
	
		