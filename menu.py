import pygame, math, sys, string, os

class Button(object):
        def __init__(self, x,y,clickType,targetImage, focused = False):
                self.height = 64
                self.width = 256
                self.pos = [x,y]
                self.nowFocused = focused
                self.name = targetImage
                self.image, self.rect = self.load_image()
                self.clickObj = clickType
                
        def draw(self,screen):
                self.image, self.rect = self.load_image()
                screen.blit(self.image, (self.pos[0], self.pos[1]))
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

class MissionSelectOnClick(OnClick):
        def isClicked(self,m):
                self.menu = m
                m.bInMissionSelect = True
                while m.bInMissionSelect:
                        self.update()
        def draw(self):
                self.menu.screen.fill((0,0,0))
                fullname = os.path.join('images', 'MissionSelect.png')
                image = pygame.transform.scale(pygame.image.load(fullname),(256, 64))
                self.menu.screen.blit(image, (172, 20 ))
                pygame.display.flip()
        def update(self):
                self.draw()
                for event in pygame.event.get():
                        self.handle_event(event)                
        def handle_event(self,event):
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                                self.menu.bInMissionSelect = False
                
                
                
	
		
class Menu(object):
        def __init__(self, screen):
                self.buttons = []
                self.bOpen = True
                self.screen = screen
                self.index = 0
                self.bInMissionSelect = False
                self.bInMenu = True
                
                
        def addButton(self, x,y,clicktype=OnClick(),targetImage = "Blank"):
               # print len(self.buttons)
                if len(self.buttons) == 0:
                        self.buttons.append(Button(x,y,clicktype,targetImage,True))
                else:
                        self.buttons.append(Button(x,y,clicktype,targetImage,False))
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
                                # print self.buttons[self.index].__class__.__name__
                                # print self.buttons[self.index].clickObj.__class__.__name__
                                self.buttons[self.index].clickObj.isClicked(self)
                        if event.key == pygame.K_ESCAPE:
                                sys.exit(0)
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:
                                self.buttons[self.index].clickObj.unclicked()
                if event.type == pygame.USEREVENT+1:
                        print "YAY!"
                        self.bInMenu = False
                if event.type == pygame.QUIT:
                        sys.exit(0)
        def update(self):
                for event in pygame.event.get():
                        self.handle_event(event)
		
	
		
