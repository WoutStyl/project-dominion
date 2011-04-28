import pygame, sys, string, random, math, operator, soldier, menu, button, map, protocoleditor, queueitem

#class GlobalGameFlag:
#    instance = None
#    def __init__(self):
#        self.flag = False
#    @staticmethod
#    def get():
#        if(GlobalGameFlag.instance == None):
#            GlobalGameFlag.instance = GlobalGameFlag()
#        return GlobalGameFlag.instance

class Game(object):
    screen_width=800
    screen_height=800  
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project Dominion")
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.clock = pygame.time.Clock()
        self.mouseIsDown = False
        self.mouseRect = pygame.Rect(0,0,0,0)
        self.upperleft = [0.0,0.0]
        self.position1 = (0.0,0.0)
        self.arrowdown = False
        self.leftdown = False
        self.rightdown = False
        self.updown = False
        self.downdown = False
        
        self.target = soldier.Soldier(float(6.0*32),float(7.0*32))
        self.target.image.fill((10,0,0))
        self.target.anim_len = 500

        self.map = map.Map.get()
        self.paused = False

        self.mainMenu = menu.MainMenu()
    def update(self, deltaSeconds):
        if self.mainMenu.bInMenu is False:
            self.paused = False
        
        self.map.update(deltaSeconds)

        if self.map.is_loaded():
            buildmenu = self.map.get_unit_menu()
        else:
            buildmenu = None

        if buildmenu is not None:
            self.mainMenu = buildmenu

        if self.leftdown and self.upperleft[0] != 0.0:
            self.upperleft[0] = self.upperleft[0] - 1
            self.mouseRect.x -= 1
        if self.rightdown and self.upperleft[0] != (1600 - self.screen_width):
            self.upperleft[0] = self.upperleft[0] + 1
            self.mouseRect.x += 1
        if self.updown and self.upperleft[1] != 0.0:
            self.upperleft[1] = self.upperleft[1] - 1
            self.mouseRect.y -= 1
        if self.downdown and self.upperleft[1] != (1600 - self.screen_height):
            self.upperleft[1] = self.upperleft[1] + 1
            self.mouseRect.y += 1
            
        if self.mouseIsDown:
            self.position2 = pygame.mouse.get_pos()
            self.position2 = (self.position2[0] + self.upperleft[0], self.position2[1] + self.upperleft[1])
            #self.position1 = (self.position1[0] + self.upperleft[0], self.position1[1] + self.upperleft[0])
            self.mouseRect = self.mouse_select(self.position1,self.position2)
            
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
        ####All key presses to game here
            if event.key == pygame.K_LEFT:
                self.leftdown = True
            if event.key == pygame.K_RIGHT:
                self.rightdown = True
            if event.key == pygame.K_UP:
                self.updown = True
            if event.key == pygame.K_DOWN:
                self.downdown = True
        
            # Escape brings up the pause menu
            if event.key == pygame.K_ESCAPE:
                if self.paused == True:
                    self.paused = False
                    self.mainMenu.bInMenu = False
                else:
                    self.paused = True
                    self.mainMenu = menu.MainMenu()

            # P brings up the protocol editor (may want to bring up
            # protocol editor through pause menu
            if event.key == pygame.K_p:
                if self.paused == True:
                    self.paused = False
                    self.mainMenu.bInMenu = False 
                elif self.paused == False:
                    self.paused = True
                    self.mainMenu = protocoleditor.ProtocolEditor()
        ####End key presses
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.leftdown = False
            if event.key == pygame.K_RIGHT:
                self.rightdown = False
            if event.key == pygame.K_UP:
                self.updown = False
            if event.key == pygame.K_DOWN:
                self.downdown = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.position1 = event.pos
                self.position1 = (self.position1[0] + self.upperleft[0], self.position1[1] + self.upperleft[1])
                self.position2 = self.position1
                self.mouseIsDown = True
                self.mouseRect = self.mouse_select(self.position1,self.position2)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.position2 = event.pos
                self.position2 = (self.position2[0] + self.upperleft[0], self.position2[1] + self.upperleft[1]) 
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
        self.screen.fill((0,0,0))
        if self.map.is_loaded():
           self.map.draw(self.screen,self.upperleft,self.mouseRect)
    def main_loop(self):
        while 1:
            self.clock.tick(50)
            deltaSeconds = self.clock.get_time()/1000.0
            if deltaSeconds > 0.08:
                deltaSeconds = 0.02
            for event in pygame.event.get():
                if not self.mainMenu.bInMenu or (not self.mainMenu.handle_event(event) and not self.mainMenu.stealInput):
                    self.handle_event(event)
            self.screen.fill((0,0,0))
            if self.mainMenu.stealInput == False or not self.mainMenu.bInMenu:
                self.game_loop(deltaSeconds)
            if self.mainMenu.bInMenu:
                self.menu_loop()
            pygame.display.flip()
    def menu_loop(self):
        self.mainMenu.check_focus()
        self.mainMenu = self.mainMenu.update()
        self.mainMenu.draw(self.screen)
        if self.map.is_loaded():
            queue = []
            queue = self.map.get_unit_queue()
            for u in queue:
                u.draw(self.screen)
        
        
    def game_loop(self, deltaSeconds):
        self.update(deltaSeconds)
        self.draw()
        
        
        
        
g = Game()

g.main_loop()
