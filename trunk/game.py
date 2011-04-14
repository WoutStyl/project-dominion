import pygame, sys, string, random, math, operator, soldier, menu, button, map
        
class Game(object):
    screen_width=600
    screen_height=600  
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project Dominion")
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self.mouseIsDown = False
        self.mouseRect = pygame.Rect(0,0,0,0)
        
        self.target = soldier.Soldier(float(6.0*32),float(7.0*32))
        self.target.image.fill((10,0,0))
        self.target.anim_len = 500

        self.map = map.Map.get()
        self.pauseMenu = menu.MainMenu(self.screen)
        self.paused = False
    def update(self):
        self.clock.tick(50)
        deltaSeconds = self.clock.get_time()/1000.0
        
        for event in pygame.event.get():
            self.handle_event(event)
        if self.paused == True:
            self.pauseMenu.update()
        self.map.update(deltaSeconds)
            
        if self.mouseIsDown:
            self.position2 = pygame.mouse.get_pos()
            self.mouseRect = self.mouse_select(self.position1,self.position2)
            
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_p:
                if self.paused == True:
                    self.paused = False
                    print("UNPAUSE")
                elif self.paused == False:
                    self.paused = True
                    print("PAUSE")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.position1 = event.pos
                self.position2 = pygame.mouse.get_pos()
                self.mouseIsDown = True
                self.mouseRect = self.mouse_select(self.position1,self.position2)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.position2 = event.pos
                self.mouseRect = self.mouse_select(self.position1,self.position2)
                self.map.select_group(self.mouseRect)
                self.mouseRect = pygame.Rect(0,0,0,0)
                self.mouseIsDown = False
            
    # Returns a properly formatted rectangle from mouse positions
    def mouse_select(self,tuple1,tuple2):
        if(tuple1[0] < tuple2[0]):
            #closer to the left
            posx = tuple1[0]
            width = tuple2[0] - tuple1[0]
        else:
            posx = tuple2[0]
            width = tuple1[0] - tuple2[0]
        #y dimension
        if(tuple1[1] < tuple2[1]):
            #closer to the top
            posy = tuple1[1]
            height = tuple2[1] - tuple1[1]
        else:
            posy = tuple2[1]
            height = tuple1[1] - tuple2[1]
            
        return pygame.Rect(posx,posy,width,height)
            
    def draw(self):
        
        
        if self.paused == True:
            self.screen.fill((0,0,0))
            self.map.draw(self.screen)
            self.pauseMenu.draw(self.screen)
        else:
            self.screen.fill((0,0,0))
            self.map.draw(self.screen)
            
        if self.mouseRect.width != 0 or self.mouseRect.height != 0:
            pygame.draw.rect(self.screen,(175,175,175),self.mouseRect,2)
        
g = Game()

bInMenu = True
m = menu.MainMenu(g.screen)

#print buttonlocx
#print buttonlocy
while 1:
    if m.bInMenu:
        m.check_focus()
        m = m.update()
        g.screen.fill((0,0,0))
        m.draw(g.screen)
        pygame.display.flip()
    else:
        g.update()
        g.draw()
        pygame.display.flip()
