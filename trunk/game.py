import pygame, sys, string, random, math, operator, soldier, menu
        
class Game(object):
    screen_width=600
    screen_height=600  
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project Dominion")
        cursor=pygame.cursors.compile(("   XX   ","   XX   ","   XX   ","XXXXXXXX","XXXXXXXX","   XX   ","   XX   ","   XX   "))
        pygame.mouse.set_cursor((8,8),(4,4),*cursor)
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.enemies = []
        for i in range(10):
            self.enemies.append(soldier.Soldier(random.randint(0,self.screen_width),random.randint(0,self.screen_height)))
        
    def update(self):
        self.clock.tick(50)
        delta_seconds = self.clock.get_time()/1000.0
        
        for event in pygame.event.get():
            self.handle_event(event)
        
        for e in self.enemies:
            e.update(delta_seconds)
            e.keep_on_screen(self.screen_width,self.screen_height)
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        
    def draw(self):
        self.screen.fill((0,0,0))
        
        for e in self.enemies:
            e.draw(self.screen)
        
        
g = Game()

bInMenu = True
m = menu.Menu()
oc = menu.StartOnClick()
buttonlocx = g.screen_width/2
buttonlocx -= 128
buttonlocy = g.screen_height/2
buttonlocy -= 32
#print buttonlocx
#print buttonlocy
m.addButton(buttonlocx, (buttonlocy -128), menu.OnClick(), "StartCampaign")
m.addButton(buttonlocx,buttonlocy,menu.StartOnClick(),"StartMission")
m.addButton(buttonlocx,(buttonlocy+128), menu.OnClick(), "LoadCampaign")
m.addButton(buttonlocx,(buttonlocy+256), menu.OnClick(), "LoadMission")
print m.index
while m.bInMenu:
    m.update()
    g.screen.fill((0,0,0))
    m.draw(g.screen)
    pygame.display.flip()

while 1:
    g.update()
    g.draw()
    pygame.display.flip()
